# BloodConnect

A web platform designed to connect voluntary blood donors with urgent hospital requests and community donation campaigns.

## Overview

**BloodConnect** bridges the gap between donors and medical institutions to facilitate life-saving blood requests. It provides a centralized, easy-to-use platform for broadcasting urgent needs based on blood type and location, organizing donation drives, and keeping donors informed when help is needed most.

## Key Features

* **Urgent Request Matching:** Post and broadcast urgent blood requirements to compatible registered donors nearby.
* **Donor & Hospital Dashboards:** Specialized portals for donors to manage their availability and for hospitals to manage active requests.
* **Donation Drives & Campaigns:** Create, discover, and participate in local blood donation events and public awareness campaigns.
* **Real-Time Alerts:** Notify registered donors when matching urgent blood requests are submitted in their area.

## Tech Stack

* **Backend:** Python & Django
* **Frontend:** HTML5, CSS3, JavaScript / Tailwind CSS
* **Database:** SQLite
* **Authentication:** Django Authentication System (Role-Based Access)

## Getting Started

### Prerequisites
* Python 3.10+
* `pip` and `venv`

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/HammamiSalmen/BloodConnect.git
cd BloodConnect

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations & start development server
python manage.py migrate
python manage.py runserver
