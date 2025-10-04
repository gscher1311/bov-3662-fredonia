#!/usr/bin/env python3.11
"""
Generate LAAA-compliant underwriting JSON for 3662 Fredonia Dr
Following buyer's perspective underwriting standards
"""

import json
from datetime import datetime

# Property details
property_address = "3662 Fredonia Dr, Studio City, CA 90068"
list_price = 1750000
units = 4
building_sf = 2530
lot_sf = 3933

# Current rent roll (from marketing sheet)
current_rents = {
    "2BR_2BA_1": 3302,
    "2BR_2BA_2": 2418,
    "Studio_1": 2095,
    "Studio_ADU": 1500
}

# Market rents (from marketing sheet)
market_rents = {
    "2BR_2BA_1": 3500,
    "2BR_2BA_2": 3500,
    "Studio_1": 2400,
    "Studio_ADU": 1800
}

# Calculate annual figures
current_monthly_rent = sum(current_rents.values())
market_monthly_rent = sum(market_rents.values())

current_annual_rent = current_monthly_rent * 12
market_annual_rent = market_monthly_rent * 12

# Vacancy rate (buyer's perspective - conservative)
vacancy_rate = 0.04  # 4%

# Calculate Effective Gross Income
current_egi = current_annual_rent * (1 - vacancy_rate)
market_egi = market_annual_rent * (1 - vacancy_rate)

# Operating Expenses (Buyer's Perspective)
# Property tax will be reassessed at purchase price
property_tax_rate = 0.0110  # 1.10% of purchase price
current_property_tax = list_price * property_tax_rate  # $19,250

# Other expenses (from marketing sheet, validated)
insurance = 3530
utilities = 4080
repairs_maintenance_rate = 0.10  # 10% of EGI (conservative)
management_rate = 0.03  # 3% of EGI
reserves_per_unit = 300
reserves = reserves_per_unit * units

# Current scenario
current_repairs = current_egi * repairs_maintenance_rate
current_management = current_egi * management_rate
current_total_expenses = (current_property_tax + insurance + utilities + 
                          current_repairs + current_management + reserves)
current_noi = current_egi - current_total_expenses
current_cap_rate = (current_noi / list_price) * 100

# Pro Forma scenario (market rents)
proforma_repairs = market_egi * repairs_maintenance_rate
proforma_management = market_egi * management_rate
proforma_total_expenses = (current_property_tax + insurance + utilities + 
                           proforma_repairs + proforma_management + reserves)
proforma_noi = market_egi - proforma_total_expenses
proforma_cap_rate = (proforma_noi / list_price) * 100

# GRM calculations
current_grm = list_price / current_annual_rent
market_grm = list_price / market_annual_rent

# Price per unit and per SF
price_per_unit = list_price / units
price_per_sf = list_price / building_sf

# Build JSON output
underwriting_data = {
    "property": {
        "address": property_address,
        "apn": "Unknown",  # Not provided in marketing sheet
        "units": units,
        "building_sf": building_sf,
        "lot_sf": lot_sf,
        "year_built": "1962/2025",
        "zoning": "Unknown"
    },
    "pricing": {
        "list_price": list_price,
        "price_per_unit": round(price_per_unit, 2),
        "price_per_sf": round(price_per_sf, 2)
    },
    "current_performance": {
        "rent_roll": current_rents,
        "monthly_rent": current_monthly_rent,
        "annual_rent": current_annual_rent,
        "vacancy_rate": vacancy_rate,
        "vacancy_loss": round(current_annual_rent * vacancy_rate, 2),
        "effective_gross_income": round(current_egi, 2),
        "operating_expenses": {
            "property_tax": round(current_property_tax, 2),
            "insurance": insurance,
            "utilities": utilities,
            "repairs_maintenance": round(current_repairs, 2),
            "management": round(current_management, 2),
            "reserves": reserves,
            "total": round(current_total_expenses, 2),
            "expense_ratio": round((current_total_expenses / current_egi) * 100, 2)
        },
        "net_operating_income": round(current_noi, 2),
        "cap_rate": round(current_cap_rate, 2),
        "grm": round(current_grm, 2)
    },
    "pro_forma_performance": {
        "rent_roll": market_rents,
        "monthly_rent": market_monthly_rent,
        "annual_rent": market_annual_rent,
        "vacancy_rate": vacancy_rate,
        "vacancy_loss": round(market_annual_rent * vacancy_rate, 2),
        "effective_gross_income": round(market_egi, 2),
        "operating_expenses": {
            "property_tax": round(current_property_tax, 2),
            "insurance": insurance,
            "utilities": utilities,
            "repairs_maintenance": round(proforma_repairs, 2),
            "management": round(proforma_management, 2),
            "reserves": reserves,
            "total": round(proforma_total_expenses, 2),
            "expense_ratio": round((proforma_total_expenses / market_egi) * 100, 2)
        },
        "net_operating_income": round(proforma_noi, 2),
        "cap_rate": round(proforma_cap_rate, 2),
        "grm": round(market_grm, 2)
    },
    "value_add_opportunity": {
        "monthly_upside": market_monthly_rent - current_monthly_rent,
        "annual_upside": market_annual_rent - current_annual_rent,
        "noi_upside": round(proforma_noi - current_noi, 2),
        "upside_percentage": round(((market_annual_rent - current_annual_rent) / current_annual_rent) * 100, 2)
    },
    "metadata": {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "underwriting_standard": "LAAA Buyer's Perspective",
        "assumptions": {
            "vacancy_rate": "4% (conservative buyer assumption)",
            "property_tax": "1.10% of purchase price (reassessed)",
            "repairs_maintenance": "10% of EGI (conservative)",
            "management": "3% of EGI",
            "reserves": "$300 per unit annually"
        }
    }
}

# Write to file
output_file = "/home/ubuntu/3662_fredonia_analysis/underwriting_output.json"
with open(output_file, 'w') as f:
    json.dump(underwriting_data, f, indent=2)

print(f"Underwriting JSON generated: {output_file}")
print(f"\nKey Metrics:")
print(f"Current NOI: ${current_noi:,.0f} ({current_cap_rate:.2f}% cap)")
print(f"Pro Forma NOI: ${proforma_noi:,.0f} ({proforma_cap_rate:.2f}% cap)")
print(f"Annual Upside: ${market_annual_rent - current_annual_rent:,.0f}")
