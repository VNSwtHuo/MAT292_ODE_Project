import torch
import pandas as pd 
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import math
from scipy.linalg import expm


# read .csv file and load data
file_path = 'FINAL_mrgsolve_simulation.csv'
df = pd.read_csv(file_path)

time_tensor = torch.tensor(df["time"].values, dtype=torch.float32)
cent_tensor = torch.tensor(df["CENT"].values, dtype=torch.float32)

timetotal = time_tensor.cpu().numpy()
centtotal = cent_tensor.cpu().numpy()

# split data to training data (80%) and testing data (20%)
split_idx = int(0.8 * len(timetotal))

times = timetotal[:split_idx]
time_test = timetotal[split_idx:]

concentrations = centtotal[:split_idx]
concen_test = centtotal[split_idx:]


## ---------- plot ----------
def plot_results(times, concentrations, c1):
    plt.figure(figsize=(8,5))

    # plot concentrations
    plt.plot(times, concentrations, '-o',alpha = 0.2, markersize=4, label='data')

    # plot c1
    plt.plot(times, c1, linestyle='-', linewidth=1.5, label='model')

    plt.axvline(x=38.4, linestyle='--', linewidth=1.5, color='blue', label='Train/Test Split')
    plt.xlabel('Time(hr)')
    plt.ylabel('Amount(mg)')
   
    plt.legend()
    plt.grid(True)

    plt.show()

def plot_error_results(times, concentrations):
    plt.figure(figsize=(8,5))
    plt.plot(times, concentrations, '-o',alpha = 0.2, markersize=4, label='error of data')

    plt.axvline(x=38.4, linestyle='--', linewidth=1.5, color='blue', label='Train/Test Split')
    plt.xlabel('Time(hr)')
    plt.ylabel('Amount Error(mg)')
   
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
    c = simulate_c(timetotal, V_opt, Q_opt)
    plot_results(timetotal,centtotal,c)
    plot_error_results(timetotal,centtotal-c)
    
    
    #calculate error for testing
    c0 = (simulate_c(timetotal, V_opt, Q_opt))[split_idx:]
    SSE = np.sum((c0 - concen_test) ** 2)
    standard_d_square = SSE/len(time_test)
    print(" MSE =",standard_d_square)
    
    
    k = 2
    n = len(time_test)
    AICc = n*math.log(SSE/n) + 2*k + 2*k*(k+1)/(n-k-1) + n*math.log(2*math.pi) + n
    BIC = n*math.log(SSE/n) + k*math.log(n) + n*math.log(2*math.pi) + n
    print(f"AICc = {AICc}")
    print(f"BIC = {BIC}")
    
    
    
    
    #calculate sensitivity
    total_time = times[-1]
    A = np.array([-Q_opt/V_opt])
    y0 = np.array([concentrations[0]])
    (best_p, best_q), max_S, S_matrix = find_max_sensitivity(A, total_time, y0)
    print(f"sensitivity matrix is {S_matrix}")
    print(f"most sensitive point is {(best_p,best_q)}, with max S of {max_S}")
    
    
else:
    print("ERROR in optimization")
    print(result.message)




