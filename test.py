import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotx
import matplotlib.pyplot as plt

# Parameters of the Heston model
kappa = 0.5  # Mean reversion speed
theta = 0.05  # Long-term volatility level
sigma = 0.1  # Volatility of volatility
rho = -0.7  # Correlation coefficient between price and volatility
v0 = 0.05  # Initial volatility value
degree = 5 # Regression's degree

# Function to simulate the Heston model
def simulate_heston(n_samples):
    dt = 1 / 252  # Time interval (1 day)
    sqrt_dt = np.sqrt(dt)
    S = np.zeros(n_samples)
    v = np.zeros(n_samples)
    S[0] = 100  # Initializing asset price with an arbitrary value
    v[0] = v0  # Initial volatility value

    # Heston model simulation
    for i in range(1, n_samples):
        dW1 = np.random.normal(0, sqrt_dt)
        dW2 = rho * dW1 + np.sqrt(1 - rho**2) * np.random.normal(0, sqrt_dt)

        v[i] = max(v[i-1] + kappa * (theta - v[i-1]) * dt + sigma * np.sqrt(max(v[i-1], 0)) * dW2, 0)
        S[i] = S[i-1] + S[i-1] * np.sqrt(max(v[i-1], 0)) * dW1

    return S

# Simulating data following the Heston model
n_samples = 10000
X = np.linspace(0, 1, n_samples).reshape(-1, 1)
y = simulate_heston(n_samples).reshape(-1, 1)

# Splitting the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Transforming the data to add polynomial features
poly_features = PolynomialFeatures(degree=degree, include_bias=False)  
X_poly_train = poly_features.fit_transform(X_train)
X_poly_test = poly_features.transform(X_test)

# Creating the Linear Regression model
model = LinearRegression()
model.fit(X_poly_train, y_train)

# Evaluating the model with the test data
score = model.score(X_poly_test, y_test)
print(f"Model score: {score}")

# Making predictions with the model
X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
X_range_poly = poly_features.transform(X_range)
y_pred_range = model.predict(X_range_poly)

# Defining new input data for projection
X_new = np.linspace(X.max(), X.max() + 0.8/degree, 20).reshape(-1, 1)  # Adjust as needed
X_new_poly = poly_features.transform(X_new)
y_new_pred = model.predict(X_new_poly)

# Visualizing the original data and projections
plt.style.use(matplotx.styles.dracula)
plt.scatter(X_test, y_test, color='white', label='Real Data', s=3000/n_samples)
plt.plot(X_range, y_pred_range, color='yellow', label='Polynomial Regression Curve')
plt.scatter(X_new, y_new_pred, color='red', label='Projections', s=8000/n_samples)
plt.xlabel('X')
plt.ylabel('y')
plt.xlim(0,max(X_new))
plt.ylim(0.9*min(min(y_test),max(min(y_new_pred),-5)), 
         1.1*max(max(y_test),max(y_new_pred) if max(y_new_pred)<2*max(y_test) else max(y_test)))
plt.title('Polynomial Regression of Degree ' + str(degree) + ' Adjusted to the Heston Model')
plt.legend()
plt.show()