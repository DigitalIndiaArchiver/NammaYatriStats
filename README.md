# NammaYatriStats

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FlatGithub](https://img.shields.io/badge/FlatGithub-View%20Data-green?style=flat-square&logo=github)](https://flatgithub.com/srikanthlogic/NammaYatriStats)
[![Open in Gitpod](https://img.shields.io/badge/Open%20in-Gitpod-blue?logo=gitpod)](https://gitpod.io/#https://github.com/srikanthlogic/NammaYatriStats)

## NammaYatri

[Namma Yatri](https://www.nammayatri.in/) is a mobility SaaS provider currently focussed on demand aggregation and supply orchestration of para-transit mobility (currently limited to auto-rickshaw) in parts of Bengaluru and Mysuru in Karnataka, India. Namma Yatri is operated by [JusPay Technologies](https://juspay.in/) and supported by [ONDC - Open Network for Digital Commerce](https://www.ondc.org/), a non-government, non-profit e-commerce company. 


Technology behind Namma Yatri is powered by *[Beckn Protocol](https://becknprotocol.io/)*, a set of specifications powering a network for demand discovery and supply orchestration built by [FIDE - Foundation for Interoperability in Digital Economy](https://fide.org/), a non-profit organisation co-founded by Nandan Nilekani

## Namma Yatri Stats Archiver

Namma Yatri publishes a set of open meta data aggregated by Assembly Constituency / Municipal Ward. This archiver runs daily to archive the published stats to enable a time-series visualisation of the data in mobility network Namma Yatri

### About Aggregate Statistics

* Following is summary of metrics published by Namma Yatri.

| S.No | File Name  | Aggregation Level | Attributes  | Update Frequency |
|------|-----------------------------|------------------------|---------------------------------------------------------------------------------|------------------|
| 1    | cumulative_stats.json       | Network Instance level | date_created,drivers_registered,no_of_completed_rides,no_of_ongoing_rides,no_of_search_request,riders_registered,total_earning  | Daily            |
| 2    | daily_stats_v2.json         | Network Instance level | no_of_search_request, no_of_completed_rides, total_earning                | Hourly           |
| 3    | driver_eda_ca.json          | Assembly Constituency  | AC_CODE,AC_NAME,active,total_active_drivers,total_active_drivers_notonride,total_drivers_on_ride| |
| 4    | driver_eda_ward.json        | Ward  | ACCESS DENIED          | ACCESS DENIED    |
| 5    | funnel_cumulative_ca.json   | Assembly Constituency  | AC_CODE,AC_NAME,avg_dist_per_trip,avg_fare,booking_cancellation_ratio,bookings_generated,cancelled_trips,completed_trips,conversation_rate,driver_earning,quote_acceptance_ratio,search_for_estimates,search_for_quotes,search_to_estimate_ratio,search_which_got_estimates,search_which_got_quotes,total_distance      | |
| 6    | funnel_cumulative_ward.json | Ward  | avg_dist_per_trip,avg_fare,booking_cancellation_ratio,bookings_generated,cancelled_trips,completed_trips,conversation_rate,driver_earning,quote_acceptance_ratio,search_for_estimates,search_for_quotes,search_to_estimate_ratio,search_which_got_estimates,search_which_got_quotes,total_distance,ward_name,ward_number| |
| 7    | funnel_live_ca.json         | Assembly Constituency  | AC_CODE,AC_NAME,avg_dist_per_trip,avg_fare,booking_cancellation_ratio,bookings_generated,cancelled_trips,completed_trips,conversation_rate,driver_earning,ongoing_trips,quote_acceptance_ratio,search_for_estimates,search_for_quotes,search_to_estimate_ratio,search_which_got_estimates,search_which_got_quotes,total_distance       | LIVE / Daily     |
| 8    | funnel_live_ward.json       | Ward  | avg_dist_per_trip,avg_fare,booking_cancellation_ratio,bookings_generated,cancelled_trips,completed_trips,conversation_rate,driver_earning,ongoing_trips,quote_acceptance_ratio,search_for_estimates,search_for_quotes,search_to_estimate_ratio,search_which_got_estimates,search_which_got_quotes,total_distance,ward_name,ward_number | LIVE / Daily     |
| 9    | trends_cumulative_ca.json   | Assembly Constituency  | AC_CODE,AC_NAME,date_created,no_of_search_request| |
| 10   | trends_cumulative_ward      | Ward  | date_created,no_of_search_request,ward_name,ward_number           | |
| 11   | trends_live_ca.json         | Assembly Constituency  | AC_CODE,AC_NAME,conversion_rate,date_created,hour_created,no_of_completed_rides,no_of_ride_booking,no_of_search_request,total_earnings       | LIVE / Daily     |
| 12   | trends_live_ward.json       | Ward  | conversion_rate,date_created,hour_created,no_of_completed_rides,no_of_ride_booking,no_of_search_request,total_earnings,ward_name,ward_number | LIVE / Daily     |

## DISCLAIMER:
This repository is provided as-is and the code within it comes with no warranty or guarantee of its effectiveness or suitability for any specific purpose. The code is provided for educational and informational purposes only and is not intended for use in production systems or for any commercial purposes. The author(s) of this repository cannot be held liable for any damages or losses incurred through the use of this code. Use at your own risk.

The author(s) are on no way related to Namma Yatri and the stats archival if for the purpose of undersight of mobility "digital public good".




