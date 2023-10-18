import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

st.info("Select your division on the left sidebar to get started!")
st.warning("Select your division on the left sidebar to get started!!!")
st.error("Select your division on the left sidebar to get started! Or scroll down for more information")

image = Image.open("./cover_image.png")
st.image(image, use_column_width="auto")

st.title("What does the model do?")
st.write("Predicts potential match outcomes.")
st.write("Assesses both offensive and defensive capabilities of teams.")

st.title("What does the model assume?")
st.write("The model assumes that past performances are indicative of future outcomes.")
st.write("Player injuries, coaching strategies, and other real-time factors are (obviously) not factored into predictions.")
st.write("The model assumes consistency in team lineup and does not account for player transfers or changes.")
st.write("Predictive accuracy may decrease with significant external changes, like changes in team strategy or playing conditions.")

st.title("Interpreting Offence/Defence Analysis Plots")

image = Image.open(f"./offence_defence.png")
st.image(image, caption=f"Example offence/defence plot", use_column_width="auto")

st.write("Displays team names on a two-dimensional grid.")
st.write("Horizontal axis (X-axis) represents offensive capabilities: Teams further to the right have demonstrated stronger offensive plays.")
st.write("Vertical axis (Y-axis) indicates defensive strength: Teams higher up are harder to score against.")
st.write("The size of each team's blob reflects variability in performance: Bigger blobs indicate more inconsistency in past games.")

st.title("Interpreting Game Predictions")

image = Image.open(f"./prediction.png")
st.image(image, caption=f"Example game outcome prediction plot", use_column_width="auto")

st.write("A table lists upcoming matches with predicted outcomes.")
st.write("Teams are paired with associated win probabilities. A higher percentage indicates a stronger prediction for that team's victory.")
st.write("Predicted scores are the model's estimate of the final game score.")
st.write("Accompanying the table is a density plot. Brighter areas show more probable score outcomes based on the model's understanding.")

st.title("Maths behind the model")

st.write("""
         This model is designed to analyze netball match outcomes by capturing both team-specific effects and the dynamics of individual matches. It's based on the Bayesian statistical framework, which means it combines prior beliefs with observed data to make inferences.

**1. Key Terms:**
- **Bayesian model:** A statistical method that applies probability to statistical problems, involving prior knowledge in addition to the current observed data.
- **Hierarchical:** A model structure where parameters are estimated at multiple levels, allowing for group-level and individual-level variations.
- **Poisson Distribution:** A probability distribution that represents the number of events in a fixed interval of time or space (e.g. the number of netball goals scored in a match!).

**2. Data Structure:**

The data consists of the number of goals scored by two competing teams in multiple matches. For each match:
- Number of goals scored by the first team.
- Number of goals scored by the second team.
- Identifier for the first and second teams.

**3. Model Parameters:**
         
- **Alpha (α):** This is the baseline log-goal rate, representing an average number of goals when there's no team-specific effect.
- **Offence[i]:** The offensive capability of team i.
- **Defence[i]:** The defensive capability of team i.

**4. Prior Distributions:**
         
Before seeing the data, we have some initial beliefs (priors) about our parameters:
- **α (Alpha):** Assumed to be drawn from a normal distribution centered at 0 with a wide standard deviation of 10.
- **Offence & Defence for each team:** Both are assumed to follow a normal distribution centered around 0, with a standard deviation of 0.5. This reflects our belief that teams are, on average, similarly competent, but there's room for variation.


**5. Random Variables and Likelihood:**
         
Let $ G_{ij} $ represent the number of goals scored by team $ i $ against team $ j $ in a given match. Given our model parameters, we express the likelihood of observing $ G_{ij} $ as follows:

- The number of goals $ G_{ij} $ scored by team $ i $ against team $ j $ follows a Poisson distribution. The log-mean rate of this distribution, denoted $ \log(\lambda_{ij}) $, is constructed as:

$$ \\log(\\lambda_{ij}) = \\alpha + \\text{offence}[i] - \\text{defence}[j] $$

Similarly,

$$ \\log(\\lambda_{ji}) = \\alpha + \\text{offence}[j] - \\text{defence}[i] $$

Where:
- $\log(\lambda_{ij}) $ is the natural logarithm of the mean rate of goals team $ i $ scores against team $ j $.
- $\\alpha$ is the baseline log-goal rate, representing the expected log number of goals in a match when there's no team-specific effect.
- $\\text{offence}[i] $ is the offensive capability of team $ i $.
- $\\text{defence}[j] $ is the defensive capability of team $ j $.

**6. Model Interpretation:**
         
- The term $ \\alpha $ acts as a global baseline for the log number of goals. It sets the average rate around which team-specific adjustments are made.
  
- The offence and defence parameters for each team allow us to adjust this baseline rate. A team with a high offence value is more likely to score goals, while a team with a high defence value is more likely to prevent the opposing team from scoring.

- The difference in offensive capability of one team and the defensive capability of their opponent ($ \\text{offence}[i] - \\text{defence}[j] $) gives an adjustment to the baseline goal rate. This means that the number of goals a team scores isn't just about their inherent capability, but also about the relative strengths and weaknesses of the teams they play against.

**7. Conclusion:**
By modeling the goals scored in matches using this Bayesian hierarchical approach, we account for both global effects (like an overall trend in scoring across all matches) and team-specific effects (how individual teams' offence and defence impact the score). This provides a comprehensive, nuanced understanding of netball match outcomes, allowing for predictions and insights that consider both general trends and specific team dynamics.
""")