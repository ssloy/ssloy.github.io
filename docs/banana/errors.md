# The Ape Learns from its mistakes

!!!tip "Key takeaway"
    Numerical physics is not about finding the solution, but about finding the best solution allowed by a hierarchy of approximations. Understanding where errors come from, how they propagate, and when they dominate is essential for interpreting results, and, crucially, knowing when not to trust them.

Solving a physics problem numerically is not a single act, but a chain of approximations.
Each link in the chain introduces its own type of error, and (important!) errors accumulate and interact.
Understanding where they come from is as important as writing correct code.

To solve a problem, first we need to model our world.
Let us review  errors that inevitably appear in virtually every setting.

## Choosing *what* equations to solve

Before any computation, we must decide how to describe the real world. This is the most fundamental (and often the largest) source of error.
We replace reality with a mathematical model (typically a PDE or ODE).
For example, here we have neglected air resistance in projectile motion.
Even when the correct physical laws are known, we often simplify them.
Once again, in this course we have reduced dimensionality (2D instead of 3D).

At this stage, no amount of numerical accuracy can fix a wrong model. If the governing equations are inappropriate, all subsequent results will be systematically biased.

## Parameter errors: choosing *which* numbers go into the model

Once the equations are chosen, they must be parameterized.
Physical constants, material properties, boundary conditions, and initial states are rarely known exactly, because we have measurement noise due to calibration errors and incomplete or indirect observations.

Even with a perfect model, uncertain parameters propagate uncertainty into the solution.

## Discretization errors: choosing *how* to represent and compute the solution

At this point, we move from continuous mathematics to computable objects.

* **Representation error:** the true solution is replaced by a finite representation.
For example, a smooth trajectory for a banana can be represented as a (non-smooth) polyline, thus introducing a geometric or functional error.
* **Equation discretization error:** the continuous equations are replaced by discrete analogues such as time-stepping schemes. We have already seen that a polyline can fairly represents a trajectory for a banana, but computing it with large $\Delta t$ creates a bias.
* **Numerical representation error:** numbers themselves are approximated. In this course we are working with a floating point representation, but oh boy, there are **plenty** of them, each one comes with its strong and weak points.
These errors are usually small locally, but can accumulate over long runs or be amplified by unstable algorithms.

## Solving a problem: optimization under imperfect information

These errors are not independent. Modeling errors set a lower bound on accuracy.
Parameter errors propagate through the dynamics.
Discretization errors compound over time or iterations.
Numerical errors may be amplified by sensitive dynamics or ill-conditioned problems.

A finer discretization cannot compensate for a wrong model, and a better integrator cannot fix poorly estimated parameters.
Improving one layer while ignoring others often leads to diminishing or misleading gains.

Once all approximations are fixed, solving a real-world physics problem almost always reduces to an optimization problem.
Explicitly or implicitly, we are searching for a state, trajectory, or set of parameters that optimizes a criterion.
For example, we can optimize for a physical criterion (energy, time, distance, cost) or fit some observations.

At this stage, new classes of errors appear:

* Objective (cost function) error: choosing an inappropriate or even a slightly wrong objective can lead to solutions that are mathematically optimal but physically irrelevant.
* Algorithmic error: optimization algorithms introduce their own limitations such as convergence to local minima instead of the global one, sensitivity to initialization etc.
* Stopping and tolerance error: practical solvers require termination criteria that can be set improperly.
* Constraint handling error: constraints may be enforced approximately, penalized incorrectly, or omitted entirely. Small violations can have large physical consequences.
* Finally, there is the irreducible layer of human error:
    * Bugs and incorrect assumptions
    * Misinterpretation of solver output
    * Copy-paste errors in formulas or code
    * Confusion between similar quantities (units, frames, conventions)

    These errors are often the hardest to detect because they produce plausible-looking results.

The problem-solving optimization stage does not sit after the error chain, it amplifies everything that came before.
The optimizer faithfully exploits the structure it is given, including all modeling, parameter, discretization, and numerical imperfections.
In practice, solving a physics problem is therefore not about “finding the solution,” but about designing an optimization process whose failures you understand and can control.

## Deliverables

This chapter does not have another deliverables but the understanding that you should train judgment rather than technique.
The goal for the course is not mastery of methods, but a simple introduction to the field, awareness of the error stack, skepticism toward results, and the habit of asking “what could be wrong?”.
Ask this question **every** time you are doing something.

