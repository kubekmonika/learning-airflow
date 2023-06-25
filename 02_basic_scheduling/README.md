# Example problem statement

Imagine we have a service that tracks user behavior on our website and allows us to analyze which pages users (identified by an IP address) accessed. For marketing purposes, we would like to know how many different pages users access and how much time they spend during each visit. To get an idea of how this behavior changes over time, we want to calculate these statistics daily, as this allows us to compare changes across different days and larger time periods.

For practical reasons, the external tracking service does not store data for more than 30 days, so we need to store and accumulate this data ourselves, as we want to retain our history for longer periods of time.