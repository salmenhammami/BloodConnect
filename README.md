# BloodConnect

A platform where hospitals post urgent blood requests and volunteer donors answer them.

The interesting part wasn't the CRUD — it was the rules. You can't donate whenever you
feel like it, so the app works out when each donor is next eligible and won't let them
respond before then. The interface is in French.

## What it does

- A hospital posts what it needs: blood group, number of bags, deadline
- Eligible donors see it and respond; the hospital confirms
- Each donor's next eligible date is calculated from their last validated donation —
  56 days for men, 84 for women
- Donors earn points and climb four tiers, from Nouveau Donneur to Sauveur d'Or
- Hospitals schedule donation campaigns and donors book a time slot
- Hospitals register with an accreditation number and stay inactive until an admin
  approves them

Donors, hospitals and admins each get their own dashboard.

**Built with** Django, SQLite and Django templates.

## Running it

```bash
git clone https://github.com/salmenhammami/BloodConnect.git
cd BloodConnect

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

New hospitals need approving before they can post anything — log into `/admin/` and
tick their `valide` flag.

## Honest notes

A coursework project. Responses show up in the dashboards but nothing is emailed yet,
matching is by city rather than by distance even though hospitals store coordinates,
and the secret key and debug flag still live in `settings.py` where they shouldn't.

---

**Salmen Hammami** · [GitHub](https://github.com/salmenhammami) · [LinkedIn](https://www.linkedin.com/in/salmenhammami/)
