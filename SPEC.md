This is a single page web app designed to illustrate standard errors.

# Basics

The title of the page is "Understanding Standard Errors".

Underneath the title are the following paragraphs:

"""
When we run a regression to estimate coefficients, each estimate is accompanied by a standard error. You can think of the standard error as how much uncertainty we have about that estimate. One way of looking at it is: if we were to re-do the regression thousands of times--each time using a different random sample of the underlying population--what would the standard deviation of all the different estimates be?

The standard error depends mostly on two things: how large is our sample size, and how tightly correlated are the X and Y variables? Generally speaking, larger sample sizes lead to lower standard errors, and noisier data leads to higher standard errors.
"""

# UI

Three panels. First panel is "Controls". Second panel is "Last 4 Samples". Third panel is "Histogram of Estimates".

## Controls

On the "Controls" panel, there is a note that says: "The true model is $Y = X\beta + \epsilon$, where $\epsilon$ has mean zero and standard deviation $\sigma$. The available controls are:

- "$\beta$". Slider from -1 to 1. Hoverable tooltip that says, "$\beta$ is the effect of X on Y, i.e. the slope of the estimated line."
- "$\sigma$". Slider from -1 to 1. Hoverable tooltip that says, "$\sigma$ is how much noise there is in the data, i.e. how tightly clustered are the points around the trend line?"
- "Sample size". Slider from 10 to 200. Integers only. Hoverable tool tip that says, "How many observations are in each sample?"

## Last 4 Samples

Shows a scatter plot with trend line for the last 4 samples simulated. Each time a new sample is run, the charts are updated.  The Y axis scale for each of these samples should be the same: from -3 to 3.  The X axis scale goes from -1 to 1.

## Histogram of Estimates

Shows a histogram for all the coefficient estimates across all samples. Also has text that says, "N estimates from N different samples". Each time a new sample is run, the histogram is updated.


# App states

The app can be in one of three states:
- Initialization
- Iteration
- Completed

## Initialization

In the initialization state, the controls are unlocked. At the bottom of the controls panel, there is a button that says "Run regression for one sample."  When the button is pressed, one sample will be simulated (draw X from uniform distribution from -1 to 1, then simulate Y values according to the model.) The estimated coefficient will be computed and added to the histogram, and the first scatter chart in the "Last 4 samples" panel will be populated.  The app state will go into "iteration".

## Iteration

In the iteration state, the controls are locked. At the bottom of the control panel, there are three buttons. 

1. "Run regression for another sample"
    - Does another simulation (drawing X from uniform distribution from -1 to 1, then simulating Y according to the model.) Adds the new estimated coefficnet to the histogram, and adds the scatter chart to the "Last 4 Samples" panel.

2. "Repeat for 1000 samples"
    - Does the simulation for randomly generated samples. Adds all the coefficients from the simulation to the histogram. Adds the last 4 samples to the "Last 4 Samples" panel. Changes state to Completed.

3. "Reset"
    - Resets the app state back to "Initialization". Clears the histogram and Last 4 Samples panel.
	
## Completed

In the completed state, the controls are unlocked. At the bottom of the control panel, there is only the Reset button.


# Tech Stack / Deployment

The simulations should be done client side, in the browser. The idea is to deploy the app via github pages.

Preference for using python with numpy / matplotlib, with pyscript, to do the simulations.

Separate files used for simulation from files used for creating the UI.  I am more likely to directly edit the simulation files than any UI related files, because I have little experience in frontend web design.

