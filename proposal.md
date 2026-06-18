Applied Causal Inference Project: Mini Research Proposal
Title and Group Members
Title: The Causal Impact of Equipment Usage on Squat Lifting Performance in Open Powerlifting
Members: Raphael Niebuhr (828154), Paul Utsch (822680)
Motivation and Research Question
Using equipment is an integral part of contests in Open Powerlifting. Supportive gear like knee wraps, single-ply and multi-ply suits promises athletes to provide a mechanical edge during challenging lifts and ultimately boost performance.

Initial correlative analysis suggests a strong causal impact of equipment usage on squat performance. However, this initial impression may be misleading: lifters who choose equipment may not be representative of the general athlete population; other variables, observed and unobserved, may contribute to both equipment choice and performance.

To simplify our research, we choose to focus on analyzing the effect of equipment usage on squat performance only, as compared to inferring a general effect of equipment on overall performance.

Thus, we ask: What is the causal effect of equipment usage on the best successful squat lift achieved, considering observed and unobserved confounders? We will tackle this problem using proven methods of causal discovery and causal effect estimation.
Data Description
Overview
For our research, we will use the OpenPowerlifting bulk dataset (snapshot 2026-05-16), which consists of around 3.9M competition entries from 1964 to 2026, across 42 columns. Within the dataset, more than 900,000 unique athletes and 33,000 unique meets are recorded. Each row represents a lifter’s performance at a specific meet. Columns include name, age, lifter’s origin, bodyweight, event, equipment, lifting performance, scores, drug-testing, sanctioning, and more. A complete overview on the columns present aside their individual description can be found under the following link https://openpowerlifting.gitlab.io/opl-csv/bulk-csv-docs.html .

There are seven distinct event categories in Open Powerlifting, each a unique combination of the three fundamental competitive disciplines “Squat”, “Bench Press”, “Deadlift”. For our analysis, we will focus exclusively on the event category that records all three and spans the most entries in our dataset compared to the other event categories; the “SBD” event category. Discipline order in the SBD event category is always the same; squats are played out first. Thus, artefacts from varying order of disciplines are not to be assumed.

Our independent variable is the categorical metric “Equipment”, with “Raw” being the reference category (strict limitations in equipment usage), “Single-ply” and “Multi-ply” representing the allowed usage of resistant body suits of either one or multiple layers, and “Wraps” describing the permitted application of resistant knee wraps, whereas the latter is only used during squats. In principle, athletes are allowed to abstain from using equipment even when competing in one of the pro-equipment categories.

In each discipline, lifters commonly get three lift attempts of which only the one with the highest weight lifted will contribute to their final score. Thus, as a metric for lifting performance, we will choose the best of the three squat attempts “Best3SquatKg”.
Preprocessing
Prior to experimentation, we will filter the existing data to remove metrics we do not need for our research. For example, the columns we will drop include “AgeClass” (we already have “Age”), the three individual attempts per discipline (we only care about the best attempt), all attempts of “Bench” and “Deadlift” (we only care about “Squat”), etc.

We will restrict the population to reduce variance in observed variables by filtering the data via constraining certain variables to a specific value that presumably avoid the influence of unobserved latent variables on our observed ones, aiming to increase the explanatory power in our experiments. Specifically, we aim to only include entries of the SBD event in which the contestant agreed to being drug-tested (which does not mean they actually got tested) and the meet was officially sanctioned. Regarding the "Federation" columns, we will replace all missing values with "Independent". 

Additionally, we will filter the data to only allow for one entry per contestant. This way, we make sure that there can be no within-contestant dependence, and observation can arguably be assumed to be independent and identically distributed.

Furthermore, we will add a new column “Year” that will be derived from “Date” to give us interval-scaling in our time metric. In this dataset, failed attempts are recorded as “negative of the attempted weight”. We will preprocess the data to overwrite all negative records in “Best3SquatKg” with 0. We will either use string encoding or one-hot encoding on “Equipment” for the discovery step.
-which independence tests can we use for multi-categorical variables vs one-hot encoded?

After filtering, remaining samples will include columns “Age”, “BodyweightKg”, “Sex”, “Equipment”, “Best3SquatKg”, “Federation”, “Event=SBD”, “Tested=Yes”, “Sanctioned=Yes”, and “Year”.

Columns can have missing values. We will remove all rows with missing values in any of the remaining columns.
Causal Assumptions
We assume the Causal Markov Condition to hold, thus we assume that all variables d-separated in the underlying causal graph given a conditioning set Z are conditionally independent in the data. We further assume faithfulness, thus we assume if variables are conditionally independent in the data their independence should be explainable by d-separation in the causal graph. As a result, we assume that conditional independence between variables in the data is equivalent to d-separation in the underlying causal graph.

We further assume causal sufficiency might not be given, in which case we explicitly embrace the possibility of unobserved confounders influencing both equipment choice and performance.

The variables in our dataset are assumed to be independent and identically distributed after making sure only one entry per contestant is given. However, this assumption may at least partly be violated, as dependence of between-contestants’ performances is principally possible. This is something we’ll keep in mind when interpreting results.

We initially assume the dependencies between variables as approximately linear-Gaussian (linear dependencies, gaussian noise) for simplicity, but will adjust our assumptions as we go since some of our variables are known to be of categorical nature while others have skewed distributions, and dependencies are yet unknown.

Several trivial assumptions will be added in the form of prior background knowledge during discovery in order to avoid unreasonable graph dependencies. These include unconditional independence of “Year”, “Sex”, and “Age”, as well as unconditional dependence between the equipment variables.
Methodological Approach
Our research path can be split into two concrete research phases: causal discovery and causal effect estimation.
Causal Discovery
We regard our data as independent observations collected over time. We explicitly do not regard our data as a time series, thus we do not model any temporal dependences, other than treating time as a covariate to practically embody dynamic latent confounders in “Year”.

We will initially use the PC algorithm as baseline discovery, for “if sufficiency held”. Then, we will use FCI as the primary discovery method allowing for potential latent confounders in the discovered graph.

Independence tests will be based initially on Fisher-Z during toy experiments, asserting linear partial correlation between variables conditioned on some set Z.

After toy modeling, in order to make sure we use appropriate independence tests, we will analyze variable distributions and correlation clouds to derive appropriate independence tests from, accounting for categorical and skewed-distribution variables as well as non-linear dependencies. Then, we will do another, more informed iteration of causal discovery.
how do we deal with the fact that conditional dependencies can have different nature than unconditioned ones?
Causal Effect Estimation
From the previously learned graph, we aim to find a backdoor-adjustment set Z that blocks all confounding paths between equipment and performance, hypothetically Z = {“Sex”, “Age”, “BodyweightKg”, “Year”}.

In the linear dependence case, we plan to estimate the effect strength of each equipment category on performance relative to “Raw” by regression of performance on all given equipment categories plus Z. This will give us an adjusted effect per category, given the assumption that Z globally blocks every backdoor path between equipment and performance.
is the global blocking assumption justified? how can we know? what would we do if not?

Wright’s Linear Path rule seems not to be a suitable alternative given the missing causal sufficiency assumption.

In the non-linear dependence case, we will research a suitable effect estimation alternative and use that.
which ones could we use? might this get too complicated?

Anticipated Challenges and Backup Plans
Discovered Causal Graphs may give results that are unreasonable, misleading or hard to interpret. We will tackle this via research for additional domain knowledge to constraint the graph further. For this, we will read through relevant literature and ask Paul’s brother, who is experienced in the sport, for expert knowledge. Additionally, we aim to resolve this by experimenting with different independence tests based on analysis of data with respect to distributions.

Discovered Causal Graphs might suggest heavy confounding; our observed variables may not sufficiently cause each other. In this case, this is in itself valuable insight, but it limits room for concrete interpretation. We will then perform additional research to see if we can derive research-based hypotheses.

We may be required to use independence tests that are computationally infeasible given the hardware we are equipped with.
Some independence tests are more computationally expensive than others, depending on the nature of dependence. In case we will have to use computationally infeasible tests, we aim to mitigate the time until convergence by further constraining the graph. This, however, may limit room for comprehensive interpretation.
Toy Model Experiments
In our initial experiments, we will try PC and FCI using Fisher-Z independence tests and initial background knowledge on the filtered dataset to get a first naive causal graph. We will then use this as a baseline for decision making to refine upon.
Timelines and Milestones
Week 1 (15.-21.06.)
Paul:
Finalize dataset preprocessing
Carefully assert correctness of processed dataset
Create variable distributions and correlation clouds
Raphael:
Analyze variable distributions and correlation clouds
Research & define appropriate independence test application
Decide/Rank appropriate independence tests for our causal discovery case

Week 2 (22.-28.06.), 🏝️Raphael
Paul:
Setup initial causal discovery experiments
Add prior background knowledge (see proposal)
Run & do initial evaluation

Week 3 (29.-05.07.), 🏝️Paul
Raphael:
Research & derive steps for iterative refinement
(detail more later)

🔥Week 4 (06.-12.07.)
Implement and run second iteration of causal discovery experiments, based on research insight & derived decisions
Setup, run, and evaluate causal effect estimation based on discovered graph

Week 5 (13.-19.07.)
Finalize causal effect estimation results
Interpret causal effect estimation results
Create informative plots with results, refine interpretations, create presentation

❗️Short Week 6 (20.-22.07.)
Practice presentation

References
Peter Spirtes and Clark Glymour, “An Algorithm for Fast Recovery of Sparse Causal Graphs”, in Social Science Computer Review, Band 9, m. 1, p. 62–72. (1995)

Peter Spirtes, Christopher Meek and Thomas Richardson, “Causal Inference in the Presence of Latent Variables and Selection Bias”, in Proceedings of the Eleventh Conference on Uncertainty in Artificial Intelligence (UAI 1995), p. 499–506.

Pearl, J. (2009). Causality. Cambridge University Press.

Datset-Link: https://openpowerlifting.gitlab.io/opl-csv/bulk-csv.html
