# 📅 DISC 212 – Class Scheduler Optimization Using ILP

## 📌 Project Overview
An academic project for DISC 212 focused on optimizing university class schedules using **Integer Linear Programming (ILP)**. Built with Python and Pulp, the system considers constraints like class timings, venue capacity, and space availability to generate the most efficient schedule possible.

I developed **Model-2**, which integrates a weighted constraint approach to achieve higher venue usage and schedule balance. Our team compared this model against the university's real schedule and an alternative model (Model-1) designed by another member. **Model-2 consistently delivered superior results.**

## 🎯 Objectives
- Maximize space utilization across available time slots and venues  
- Account for constraints: seating capacity, venue availability, class strength, and scheduling patterns  
- Generate venue-specific insights including average usage and class distributions  
- Compare scheduling outcomes across models and real-world data

## 🔍 Key Features
- Optimized scheduling using `pulp_cbc_cmd` solver  
- Comparative visualizations (bar charts, heatmaps) for MW/TR course spread and venue performance  
- Venue-level utilization stats showing mean classes and average capacity usage  
- Evaluation of scheduling quality across three models

## 🛠️ Technologies Used
- Python  
- Pulp (ILP solver)  
- Pandas & NumPy  
- Matplotlib  
- Jupyter Notebook

## 📊 Future Enhancements
- Include instructor preferences and teaching patterns  
- Add event types (lectures, labs, night classes, etc.)  
- Integrate support for venue pre-bookings and non-teaching usage

## 📂 Repository Structure
```
├── RO                                 # University's schedule stats
├── model_1                            # Alternative model by another team member
├── model_2                            # Optimized model using ILP (Usama's contribution) with MW/TR schedule and stats
├── evaluation.ipynb                   # Visual comparisons of all models and venue/course stats
├── dataset (courses.csv, venues.csv)  # Input dataset (venue, courses, schedule info) extracted from university's website
├── README.md                          # Documentation and project overview
```
