# Behavioral Interview Preparation

`Behavioral_Interview_Prep.pdf` is a personal behavioral interview prep
system built from the account holder's real projects (LedgerCore, the
Financial Account Aggregation API, FarmLink, Robotics Club, and the KNUST
CS Open Source Community). It is not application code for this project;
it lives here because it was generated during a session against this
repository.

The document is a working system, not a set of answers to memorize: every
story card that needed a specific detail this session didn't have access
to (an exact number, a specific incident, a specific quote) is marked with
a `[FILL IN]` placeholder rather than an invented fact. Fill those in
honestly before relying on the document.

To regenerate the PDF after editing content:

```bash
pip install reportlab
python3 generate_pdf.py
```

This writes `Behavioral_Interview_Prep.pdf` in the current directory.
