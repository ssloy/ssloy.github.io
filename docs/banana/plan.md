# plan

## 1. The Ape Counts Seconds

### Goal

Understand motion as a step-by-step time evolution.

### Tasks

* Define the state $(x,y,v_x,v_y)$
* Implement Euler time stepping with a fixed $\Delta t = 1$.
* Simulate until the banana goes below the ground

### Concepts

* ODE as “what happens next”
* Discretization in time
* Separation of horizontal and vertical motion

### Deliverables

- Table of $(t,x,y)$
- Plot of $x(t)$, $y(t)$ and the trajectory in the $(x,y)$ plane

## 2. The Ape Misses the Ground

### Goal

Understand event timing in a discrete-time simulation.

### Tasks

* Detect when $y$ changes sign
* Estimate landing time:
    * without interpolation
    * with linear interpolation
* Compare the two

### Concepts

* Event detection
* Sampling error
* Difference between trajectory error and event-time error

### Deliverables

* Landing time estimates
* Range estimates


## 3. The Ape Buys a Better Watch

### Goal

Study the effect of time-step refinement.

### Tasks

* Repeat simulations with smaller $\Delta t$
* Observe convergence of:
    * trajectory
    * impact time
    * range
* Combine refinement **and** interpolation

### Concepts

* Numerical convergence
* Controlled approximation
* Role of $\Delta t$

### Deliverables

* Overlaid trajectories
* Short explanation of observed convergence


## 4. The Ape Throws Farther

### Goal

Maximize horizontal range with fixed initial speed.

### Tasks

* Fix $|v_0|$
* Parametrize throw by angle
* Compute range numerically
* Maximize range using
    * grid search
    * ternary search

### Concepts

* One-dimensional optimization
* Objective functions from simulations
* No analytical derivatives

### Deliverables

* Optimal angle
* Range vs angle plot


## 5. The Lazy Ape

### Goal

Hit a target using minimal effort.

### Tasks

* Define effort as $|v_0|$
* Build a penalized cost function
* Optimize over $(v_x,v_y)$) using coordinate descent
* Visualize the cost landscape

### Concepts

* Constrained optimization
* Penalization
* Black-box simulation inside optimization

### Deliverables

* Optimal initial velocity
* Contour plot of the objective

## 6. **The Jungle Is Windy**

### Goal

Extend the model and observe its consequences.

### Tasks

* Add constant wind
* Add time-dependent wind
* Repeat:

  * range maximization
  * minimal-effort target hitting

### Concepts

* Model extension
* Non-autonomous ODEs
* Coupling effects

### Deliverables

* Trajectory comparisons
* Qualitative discussion of wind effects

---

## 7. **The Ape Learns to Look Ahead**

*(Why Euler starts to struggle)*

### Goal

Choose a better numerical method when the model becomes harder.

### Tasks

* Observe Euler bias with wind or drag
* Implement RK2 (midpoint method)
* Compare Euler and RK2 for equal (\Delta t)

### Concepts

* Local vs global error
* Method order
* Model-dependent method choice

### Deliverables

* Side-by-side Euler vs RK2 results
* Justified choice of integrator

---

## 8. **The Ape Watches and Learns**

*(Inverse problems — three stages)*

### 8.1 Find gravity (g) (no wind, no friction)

**Goal**
Estimate gravity from trajectory data.

**Tasks**

* Given ((t_i,x_i,y_i)), build a least-squares cost
* Use numerical integration inside the cost
* Estimate (g)

**Concepts**

* Inverse problems
* Least squares
* Identifiability

---

### 8.2 Fix friction, estimate (g) and constant wind

**Goal**
Estimate multiple parameters with a more complex model.

**Tasks**

* Add linear drag
* Estimate (g) and wind simultaneously
* Analyze parameter coupling

**Concepts**

* Multi-parameter estimation
* Conditioning
* Correlated parameters

---

### 8.3 Estimate gravity, wind, and friction

**Goal**
Understand the limits of parameter estimation.

**Tasks**

* Fit all three parameters
* Study sensitivity to noise and time sampling
* Observe instability or bias

**Concepts**

* Overparameterization
* Model inadequacy
* Practical identifiability

---

### Deliverables (for Chapter 8)

* Estimated parameters
* Residual plots
* Discussion of what can and cannot be identified



































3. Key pedagogical lessons

    Residual structure reveals model error

        Random residuals → measurement noise

        Structured residuals → missing physics

    Good fit ≠ correct model

        You can have a low cost even if the model is physically wrong

    Parameter estimates are conditional on model assumptions

        Emphasizes: “parameters only make sense relative to the model used”

    Visualization is crucial

        Overlaying trajectories and plotting residuals immediately shows the mismatch

4. Optional student exercise

    Generate trajectory with time-dependent wind

    Fit constant wind model using Euler integration

    Plot:

        Fitted vs true trajectory

        Residuals vs time

        Estimated parameter vs true value

Expected observation:
Residuals show systematic pattern; fitted parameter does not match true wind; trajectory mismatch grows over time.
