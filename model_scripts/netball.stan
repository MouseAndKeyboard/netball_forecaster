data {
  int<lower=1> N;           // number of observations (matches)
  int<lower=0> goals[N, 2]; // goals[i, 1] = goals by team_1 in match i, goals[i, 2] = goals by team_2 in match i
  int<lower=1> team_1[N];   // identifier for the first team in each match
  int<lower=1> team_2[N];   // identifier for the second team in each match
  int<lower=1> T;           // number of teams
}

parameters {
  real alpha;                      // intercept
  vector[T] offence;               // offence capabilities for each team
  vector[T] defence;               // defence capabilities for each team
}

model {
  // Priors
  alpha ~ normal(0, 10);
  offence ~ normal(0, 0.5);
  defence ~ normal(0, 0.5);
  
  // Likelihood
  for (i in 1:N) {
    goals[i, 1] ~ poisson_log(alpha + offence[team_1[i]] - defence[team_2[i]]);
    goals[i, 2] ~ poisson_log(alpha + offence[team_2[i]] - defence[team_1[i]]);
  }
}

generated quantities {
  int y_rep[T, T, 2];  // simulated (replicated) data for each observation
  
  for (i in 1:T) {
    for (j in 1:T) {
        y_rep[i, j, 1] = poisson_log_rng(alpha + offence[i] - defence[j]);
        y_rep[i, j, 2] = poisson_log_rng(alpha + offence[j] - defence[i]);
    }
  }
}
