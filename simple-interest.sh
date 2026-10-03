#!/bin/bash

# Simple Interest Calculator Script in Bash
# Formula: Simple Interest = (Principal * Rate * Time) / 100

echo "=========================================="
echo "        Simple Interest Calculator       "
echo "=========================================="

# Input fields: Principal, Rate of Interest, and Time Period
read -p "Enter Principal Amount (P): " principal
read -p "Enter Rate of Interest per annum (R in %): " rate
read -p "Enter Time Period in years (T): " time_period

# Calculate Simple Interest using bc for floating point calculations
interest=$(echo "scale=2; ($principal * $rate * $time_period) / 100" | bc)
total_amount=$(echo "scale=2; $principal + $interest" | bc)

echo "------------------------------------------"
echo "Principal Amount : $principal"
echo "Interest Rate    : $rate%"
echo "Time Period      : $time_period years"
echo "------------------------------------------"
echo "Simple Interest  : $interest"
echo "Total Amount     : $total_amount"
echo "=========================================="
