# Wallet + Ledger (Immutable Accounting API)

## Overview

* Wallet + Ledger is a backend API built with Django + Django REST Framework that implements a digital wallet system using an immutable ledger-based accounting model.

The core principle of this system is:

* **Balances are never updated directly.**
  The wallet balance is always derived from immutable ledger entries.

This project is designed to model real-world financial system constraints such as atomicity, idempotency, concurrency control, and double-spend prevention.
