import torch
import pandas as pd 
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import math
from scipy.linalg import expm

## take in data
data = pd.read_csv('/Users/liuhaoyu/Documents/MAT292_ODE_Project/USETHIS_Simulation_output.csv')

t_np = data['time'].values.astype(np.float32)
C_np = data['CENT'].values.astype(np.float32)

# Remove missing concentration values
mask = ~np.isnan(C_np)
t_np = t_np[mask]
C_np = C_np[mask]

N = 11
t_np = t_np[:N]
C_np = C_np[:N]

# FIX: ensure strictly increasing time
t_np, unique_idx = np.unique(t_np, return_index=True)
C_np = C_np[unique_idx]

# Normalize time
t0 = t_np.min()
t = torch.tensor((t_np - t0) / (t_np.max() - t0), dtype=torch.float32)
# concentration tensor
C = torch.tensor(C_np.reshape(-1,1), dtype=torch.float32)





times =  t.cpu().numpy()
concentrations = C.cpu().numpy()

## ---------- plot ----------
def plot_results(times, concentrations, c1):
    plt.figure(figsize=(8,5))

    # plot concentrations
    plt.plot(times, concentrations, 'o-', label='concentrations')

    # plot c1
    plt.plot(times, c1, 'o-', label='c1')

    plt.xlabel('Time')
    plt.ylabel('Concentration')
    plt.title('Comparison of Two Curves')
    plt.legend()
    plt.grid(True)

    plt.show()
    
    
## model
# ---------- define input function u(t) ----------
def u(t):
    return 0


# ---------- define model ----------
def simulate_c(times, V, Q):
    # solve ODE dc/dt = (u(t) - Q*c) / V using given V,Q through Eula method
    
    c0 = [concentrations[0]]  # initial value
    for i in range(1, len(times)):
        dt = times[i] - times[i - 1]
        dc_dt = (u(times[i - 1]) - Q * c0[-1]) / V
        c_next = c0[-1] + dc_dt * dt
        c0.append(c_next)
    return np.array(c0)


# ---------- define error ----------
def objective(params):
    V, Q = params
    c0 = simulate_c(times, V, Q)
    square = np.sum((c0 - concentrations) ** 2)
    return square


# ---------- adjusting parameters ----------
initial_guess = [1, 0.1]  # initial guess
result = minimize(objective, initial_guess, method='Nelder-Mead')





# ---------- calculate sensitivity -----------
def compute_sensitivity_matrix(A, t, y0, num_steps=100):
    """
    Compute S_pq(t) for all p, q for system y' = Ay
    S_pq(t) = || ∫0^t e^{A(t-s)} E_pq e^{As} y0 ds ||
    """

    n = A.shape[0]
    dt = t / num_steps

    # Precompute exp(As) for all s (s grid)
    s_values = np.linspace(0, t, num_steps)
    expAs_list = [expm(A * s) for s in s_values]
    expAts_list = [expm(A * (t - s)) for s in s_values]

    # storage for S_{pq}
    S = np.zeros((n, n))

    # Loop over p, q
    for p in range(n):
        for q in range(n):
            # E_pq matrix
            E = np.zeros((n, n))
            E[p, q] = 1.0

            # integral accumulator
            integral = np.zeros(n)

            # Riemann sum approximation
            for i in range(num_steps):
                expAts = expAts_list[i]
                expAs  = expAs_list[i]
                term = expAts @ (E @ (expAs @ y0))
                integral += term * dt

            S[p, q] = np.linalg.norm(integral)

    return S

def find_max_sensitivity(A, t, y0):
    S = compute_sensitivity_matrix(A, t, y0)
    p, q = np.unravel_index(np.argmax(S), S.shape)
    return (p, q), S[p, q], S







## ---------- output result ----------
if result.success:
    #model prediction and plot
    V_opt, Q_opt = result.x
    print("successfully optimize!")
    print(f" V = {V_opt:.6f}")
    print(f" Q = {Q_opt:.6f}")
    print(f" RSS = {result.fun:.6f}")
    plot_results(times, concentrations, simulate_c(times, V_opt, Q_opt))
    
    
    #calculate error
    c0 = simulate_c(times, V_opt, Q_opt)
    Rss = np.sum((c0 - concentrations) ** 2)
    
    standard_d_square = Rss/len(times)
    likelyhood = -0.5*len(times)*(math.log(2*math.pi)+1+math.log(standard_d_square))
    k = 2
    AIC = -2*likelyhood + 2*k
    BIC = -2*likelyhood + k*math.log(len(times))
    AICc = AIC + 2*k*(k+1)/(len(times)-k-1)
    print(f"AIC = {AIC}")
    print(f"BIC = {BIC}")
    print(f"AICc = {AICc}")
    
    
    #calculate sensitivity
    total_time = times[-1]
    A = np.array([-Q_opt/V_opt])
    y0 = c0[0]
    (best_p, best_q), max_S, S_matrix = find_max_sensitivity(A, total_time, y0)
    print(f"sensitivity matrix is {S_matrix}")
    print(f"most sensitive point is {(best_p,best_q)}, with max S of {max_S}")
    
else:
    print("ERROR in optimization")
    print(result.message)




