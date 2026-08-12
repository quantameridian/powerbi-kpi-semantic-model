# Report Pages

The PBIR report has two pages. Both are bound directly to objects in the local TMDL model.

## Executive Summary

The first page opens with one service area slicer and a four value card for open items, current backlog, overdue active work and SLA met rate. A monthly line chart compares reconstructed backlog with completed work. The right side shows overdue work by service area and a compact item table.

The page is meant for a service review, not detailed investigation. It makes the current pressure visible, then gives enough period and service context to decide where the next question belongs.

## Assurance Detail

The second page puts data readiness beside the record context. Its four value card shows missing owners, missing due dates, closed work without evidence and the overall readiness rate. A service area chart shows where issue records sit, while the table exposes the dimensions and source flags needed to investigate them.

The page does not imply that a low readiness rate is poor service performance. It is a warning about how much confidence should be placed in the performance result.

## Interaction

The service area slicer on the first page filters all business visuals through the `Service Area` dimension. Report users can use the normal page tabs to move to assurance detail. No hidden navigation page, bookmark state or custom visual is required.

Rendered behaviour remains part of `desktop-acceptance-test.md`; PBIR validation confirms structure and bindings but cannot replace a visual check.
