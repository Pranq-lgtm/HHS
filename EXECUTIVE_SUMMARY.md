# Executive Summary

## HHS Unaccompanied Children Program: Operational Data Review

### Purpose

This review translates the supplied HHS operational extract into decision-ready findings for government stakeholders. It is descriptive and intended to support capacity planning, oversight, and data-governance decisions.

### At a glance

- **720 reported observations** from **January 12, 2023 to December 21, 2025**
- **11,516**: maximum reported children in HHS care, on December 20, 2023
- **2,484**: children in HHS care in the final reported observation
- **67,337**: sum of reported apprehension observations
- **124,853**: sum of reported discharge observations
- **333**: maximum single reported apprehension observation

### What the data says

1. **Program scale changed materially.** Reported HHS care reached 11,516 at its observed maximum and was 2,484 at the endpoint, approximately 77% lower than that maximum.
2. **Demand is uneven.** Apprehensions range from 0 to 333 per observation; CBP custody ranges from 7 to 531. Planning from an average alone risks under-preparing for peaks.
3. **Late 2025 is lower-volume but not zero-volume.** The final observation still includes 2,484 children in HHS care and continuing custody movement and discharges.
4. **February 2024 merits review.** The largest apprehension, CBP-custody, and transfer-out observations cluster in that period. The file does not establish why.
5. **The data is not a daily census.** There are 720 rows across 1,075 calendar days. Missing dates must not be interpreted as zero activity.

### Decisions recommended

**Authorize a rolling operational watchlist.** Track HHS care, apprehensions, transfers, and discharges with 30-observation medians and high-percentile thresholds. Escalate when two or more measures exceed threshold together.

**Require data-definition controls.** Before using these fields for formal performance targets, document whether each value is a point-in-time count, an event count, or a period total. Publish cadence, revision history, and missing-date treatment.

**Plan for surge and baseline capacity.** Use the observed range and scenario bands, not the full-period average alone, to plan beds, staffing, transport, and case-management resources.

**Expand the public data responsibly.** Where lawful and privacy-preserving, add capacity, occupied beds, pending placements, length of stay, and discharge pathway. Avoid personally identifiable information and small-cell disclosure.

### Risks and caveats

- Sums across observations are not unique-child totals.
- Aggregate data cannot explain causes or outcomes.
- The difference between custody and transfer totals is not a backlog measure without aligned timing definitions.
- The source extract may be revised; decisions should reference a release date and file version.

### Suggested 90-day action plan

| Priority | Action | Owner type | Success measure |
|---|---|---|---|
| 1 | Adopt weekly dashboard review and exception thresholds | Program operations | Review cadence documented and exceptions logged |
| 2 | Run automated schema and data-quality checks | Data governance | No unreviewed duplicate, missing, or invalid records |
| 3 | Publish a field dictionary and cadence note | Transparency/data team | Public release includes definitions and revision policy |
| 4 | Develop surge scenarios using rolling percentiles | Capacity planning | Staffing and placement plans include peak scenarios |

**Bottom line:** The extract shows a substantial reduction from the observed 2023 peak in HHS care, but persistent operational demand and high variability. The safest policy response is disciplined monitoring, explicit surge planning, and stronger metadata before turning descriptive indicators into formal targets.

Source: [HHS.gov](https://www.hhs.gov/). See the full [research paper](./RESEARCH_PAPER.md) for methods, tables, findings, and limitations.
