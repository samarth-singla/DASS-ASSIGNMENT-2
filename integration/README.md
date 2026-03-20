## Integration Testing (Part 2.2)

This folder contains integration tests that validate interactions between modules in the StreetRace Manager implementation.

## Modules Under Integration

- Registration Module
- Crew Management Module
- Inventory Module
- Race Management Module
- Results Module
- Mission Planning Module
- Vehicle Maintenance Module
- Sponsorship and Budget Module

## Coverage Execution

Commands used:

1. `python -m coverage erase`
2. `python -m coverage run -m unittest discover -s integration/tests -p "test_*.py"`
3. `python -m coverage run --append -m unittest discover -s "integration/integrationn tests" -p "test_*.py"`
4. `python -m coverage report -m integration/code/*.py`

Final result for `integration/code/*.py`: **100% coverage**.

Total integration test cases in `integration/integrationn tests`: **43**.

## Integration Test Case Details

### File: test_integration_driver_race_results.py

#### TC-IR-01: register_enter_race_record_results_success
- What scenario is being tested: Register drivers, enter race, record race results, verify prize and vehicle release.
- Which modules are involved: Registration, Race Management, Results, Inventory.
- The expected result: Entrants are accepted, race completes, prize is added to cash, vehicles become available again.
- The actual result after testing: Passed. Cash moved from 1000 to 1350, race marked completed, all race vehicles available.
- Any errors or logical issues found: None.

#### TC-IR-02: enter_race_without_registered_driver_raises
- What scenario is being tested: Attempting race entry with a non-existent driver id.
- Which modules are involved: Race Management, Registration.
- The expected result: Validation error is raised.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IR-03: enter_race_with_non_driver_role_raises
- What scenario is being tested: Attempting race entry with a registered but non-driver role member.
- Which modules are involved: Registration, Race Management.
- The expected result: Validation error is raised because only drivers can enter races.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IR-04: record_results_requires_all_entrants
- What scenario is being tested: Recording results with incomplete participant list.
- Which modules are involved: Race Management, Results.
- The expected result: Validation error for missing entrants.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

### File: test_integration_mission_and_roles.py

#### TC-IM-01: create_and_start_mission_with_required_roles
- What scenario is being tested: Mission starts successfully when all required roles are available.
- Which modules are involved: Registration, Crew Management, Mission Planning.
- The expected result: Mission is marked as started.
- The actual result after testing: Passed. Mission `started=True`.
- Any errors or logical issues found: None.

#### TC-IM-02: mission_start_fails_when_role_missing
- What scenario is being tested: Mission start attempt where strategist role is missing.
- Which modules are involved: Mission Planning, Crew Management.
- The expected result: Validation error for missing required role.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IM-03: assign_role_then_start_mission
- What scenario is being tested: Role reassignment followed by mission start.
- Which modules are involved: Registration, Crew Management, Mission Planning.
- The expected result: After assigning strategist role, mission should start.
- The actual result after testing: Passed. Mission started after role assignment.
- Any errors or logical issues found: None.

#### TC-IM-04: set_skill_then_list_by_role
- What scenario is being tested: Skill update and role-based listing consistency.
- Which modules are involved: Crew Management, Registration.
- The expected result: Driver remains in driver list and updated skill is retained.
- The actual result after testing: Passed. Role filter returned correct member and skill value.
- Any errors or logical issues found: None.

### File: test_integration_budget_and_maintenance.py

#### TC-IB-01: sponsor_payout_then_repair_updates_cash
- What scenario is being tested: Sponsor payout increases cash, then repair consumes cash and parts.
- Which modules are involved: Sponsorship and Budget, Vehicle Maintenance, Inventory.
- The expected result: Correct final cash, reduced parts, and improved vehicle condition.
- The actual result after testing: Passed. Cash=750, part quantity reduced correctly, condition increased to 85.
- Any errors or logical issues found: None.

#### TC-IB-02: penalty_and_repair_can_fail_on_cash
- What scenario is being tested: Cash penalty followed by a repair that exceeds remaining funds.
- Which modules are involved: Sponsorship and Budget, Vehicle Maintenance, Inventory.
- The expected result: Repair operation fails with insufficient cash validation.
- The actual result after testing: Passed. `ValueError` was raised by cash validation.
- Any errors or logical issues found: None.

#### TC-IB-03: add_tool_and_part_integration_state
- What scenario is being tested: Combined inventory updates for tools and parts.
- Which modules are involved: Inventory.
- The expected result: Tool and part counts are persisted in inventory state.
- The actual result after testing: Passed. Quantities matched expected values.
- Any errors or logical issues found: None.

#### TC-IB-04: apply_wear_then_full_restore_cap
- What scenario is being tested: Vehicle wear and repair with condition cap at 100.
- Which modules are involved: Vehicle Maintenance, Inventory.
- The expected result: Repaired condition does not exceed 100.
- The actual result after testing: Passed. Condition capped at 100.
- Any errors or logical issues found: None.

### File: test_integration_error_paths_coverage.py

#### TC-IE-01: registration_empty_name_and_get_missing
- What scenario is being tested: Invalid registration input and missing member lookup.
- Which modules are involved: Registration.
- The expected result: Both operations raise validation errors.
- The actual result after testing: Passed. `ValueError` raised for both checks.
- Any errors or logical issues found: None.

#### TC-IE-02: race_not_found_and_vehicle_validation_paths
- What scenario is being tested: Race not found and vehicle not found during race entry.
- Which modules are involved: Race Management, Registration, Inventory.
- The expected result: Validation errors are raised.
- The actual result after testing: Passed. Both invalid paths raised `ValueError`.
- Any errors or logical issues found: None.

#### TC-IE-03: results_invalid_race_and_negative_prize
- What scenario is being tested: Results submission for invalid race and negative prize.
- Which modules are involved: Results, Race Management, Inventory.
- The expected result: Validation errors are raised.
- The actual result after testing: Passed. Both validations raised `ValueError`.
- Any errors or logical issues found: None.

#### TC-IE-04: inventory_negative_quantity_paths
- What scenario is being tested: Negative quantities for parts/tools and invalid vehicle availability update.
- Which modules are involved: Inventory.
- The expected result: Validation errors are raised.
- The actual result after testing: Passed. All invalid operations raised `ValueError`.
- Any errors or logical issues found: None.

#### TC-IE-05: mission_create_and_start_invalid_paths
- What scenario is being tested: Empty mission title, empty required roles, and missing mission start.
- Which modules are involved: Mission Planning.
- The expected result: Validation errors are raised for all invalid inputs.
- The actual result after testing: Passed. All checks raised `ValueError`.
- Any errors or logical issues found: None.

#### TC-IE-06: sponsorship_invalid_paths
- What scenario is being tested: Invalid sponsor contract inputs and invalid payout/penalty operations.
- Which modules are involved: Sponsorship and Budget, Inventory.
- The expected result: Validation errors are raised.
- The actual result after testing: Passed. All invalid operations raised `ValueError`.
- Any errors or logical issues found: None.

#### TC-IE-07: maintenance_invalid_paths
- What scenario is being tested: Invalid wear and repair inputs across all guarded maintenance branches.
- Which modules are involved: Vehicle Maintenance, Inventory.
- The expected result: Validation errors are raised for each invalid case.
- The actual result after testing: Passed. All invalid maintenance operations raised `ValueError`.
- Any errors or logical issues found: None.

### File: test_integration_duplicate_and_sorting.py

#### TC-ID-01: registration_duplicate_name_blocks_second_member
- What scenario is being tested: Duplicate registration with case-insensitive same name.
- Which modules are involved: Registration.
- The expected result: Second registration is rejected.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-ID-02: leaderboard_sort_order_for_tie_points
- What scenario is being tested: Leaderboard sorting when two drivers have equal points.
- Which modules are involved: Results, Registration.
- The expected result: Sorted by points descending, then driver id ascending.
- The actual result after testing: Passed. Leaderboard order matched expected tie rule.
- Any errors or logical issues found: None.

#### TC-ID-03: set_skill_rejects_out_of_range_level
- What scenario is being tested: Skill update beyond allowed upper bound.
- Which modules are involved: Crew Management, Registration.
- The expected result: Validation error for invalid skill level.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

### File: test_integration_reuse_vehicle_cycles.py

#### TC-IV-01: vehicle_unavailable_immediately_after_entry
- What scenario is being tested: Vehicle state immediately after race entry.
- Which modules are involved: Race Management, Inventory, Registration.
- The expected result: Entered vehicle becomes unavailable.
- The actual result after testing: Passed. Availability changed to `False`.
- Any errors or logical issues found: None.

#### TC-IV-02: vehicle_released_after_result_submission
- What scenario is being tested: Vehicle release after race results are recorded.
- Which modules are involved: Race Management, Results, Inventory.
- The expected result: All entrant vehicles become available.
- The actual result after testing: Passed. Availability returned to `True`.
- Any errors or logical issues found: None.

#### TC-IV-03: reuse_same_vehicle_in_new_race_after_release
- What scenario is being tested: Reusing a vehicle in a second race after first race completion.
- Which modules are involved: Race Management, Results, Inventory.
- The expected result: Vehicle can be entered again after release.
- The actual result after testing: Passed. Second race entry succeeded.
- Any errors or logical issues found: None.

### File: test_integration_contract_case_rules.py

#### TC-IC-01: duplicate_contract_check_is_case_insensitive
- What scenario is being tested: Sponsor duplicate detection with different text case.
- Which modules are involved: Sponsorship and Budget.
- The expected result: Duplicate sponsor contract is rejected.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IC-02: receive_payout_requires_exact_registered_key
- What scenario is being tested: Payout request with wrong sponsor key case.
- Which modules are involved: Sponsorship and Budget, Inventory.
- The expected result: Payout fails for unknown contract key.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IC-03: penalty_then_payout_keeps_budget_consistent
- What scenario is being tested: Budget consistency after penalty then payout.
- Which modules are involved: Sponsorship and Budget, Inventory.
- The expected result: Final cash reflects both operations in correct sequence.
- The actual result after testing: Passed. Final cash matched expected value.
- Any errors or logical issues found: None.

### File: test_integration_mission_lifecycle_guards.py

#### TC-IL-01: start_mission_twice_raises_error
- What scenario is being tested: Starting an already started mission.
- Which modules are involved: Mission Planning.
- The expected result: Second start attempt is rejected.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IL-02: list_by_role_returns_empty_for_unknown_role
- What scenario is being tested: Role listing for role with no members.
- Which modules are involved: Crew Management, Registration.
- The expected result: Empty list is returned.
- The actual result after testing: Passed. Empty list observed.
- Any errors or logical issues found: None.

#### TC-IL-03: create_mission_normalizes_role_text
- What scenario is being tested: Mission role normalization for extra spaces/case.
- Which modules are involved: Mission Planning.
- The expected result: Required roles are normalized to lowercase trimmed values.
- The actual result after testing: Passed. Normalized role list matched expected.
- Any errors or logical issues found: None.

### File: test_integration_results_points_progression.py

#### TC-IP-01: points_accumulate_across_two_races
- What scenario is being tested: Multi-race points accumulation.
- Which modules are involved: Registration, Race Management, Results, Inventory.
- The expected result: Drivers retain cumulative points across races.
- The actual result after testing: Passed. Points matched expected totals.
- Any errors or logical issues found: None.

#### TC-IP-02: cash_accumulates_with_multiple_prizes
- What scenario is being tested: Multiple race prize pools update cash over time.
- Which modules are involved: Results, Inventory, Race Management.
- The expected result: Cash balance increases by sum of prize pools.
- The actual result after testing: Passed. Final cash matched expected value.
- Any errors or logical issues found: None.

#### TC-IP-03: leaderboard_after_multiple_races
- What scenario is being tested: Leaderboard correctness after more than one race.
- Which modules are involved: Results, Registration.
- The expected result: Highest cumulative points appears first.
- The actual result after testing: Passed. Leaderboard top entry matched expected driver.
- Any errors or logical issues found: None.

#### TC-IP-04: completed_race_rejects_second_record
- What scenario is being tested: Double submission of results for same race.
- Which modules are involved: Results, Race Management.
- The expected result: Second submission is rejected.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

### File: test_integration_inventory_cash_boundaries.py

#### TC-IQ-01: cash_can_reach_exact_zero
- What scenario is being tested: Cash update to exact zero boundary.
- Which modules are involved: Inventory.
- The expected result: Operation succeeds and balance becomes 0.
- The actual result after testing: Passed. Balance became 0.
- Any errors or logical issues found: None.

#### TC-IQ-02: cash_cannot_go_below_zero
- What scenario is being tested: Cash update below zero boundary.
- Which modules are involved: Inventory.
- The expected result: Validation error for insufficient cash.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IQ-03: payout_recovers_after_near_zero
- What scenario is being tested: Sponsor payout recovering low cash state.
- Which modules are involved: Sponsorship and Budget, Inventory.
- The expected result: Payout increases balance correctly.
- The actual result after testing: Passed. Balance increased to expected value.
- Any errors or logical issues found: None.

#### TC-IQ-04: repair_with_exact_remaining_cash_succeeds
- What scenario is being tested: Repair transaction consuming exactly remaining cash.
- Which modules are involved: Vehicle Maintenance, Inventory.
- The expected result: Repair succeeds and balance reaches exact zero.
- The actual result after testing: Passed. Repair succeeded and balance became 0.
- Any errors or logical issues found: None.

### File: test_integration_role_transition_effects.py

#### TC-IT-01: mechanic_cannot_enter_race_before_role_change
- What scenario is being tested: Race entry blocked for non-driver role.
- Which modules are involved: Registration, Race Management.
- The expected result: Entry is rejected.
- The actual result after testing: Passed. `ValueError` was raised.
- Any errors or logical issues found: None.

#### TC-IT-02: member_can_enter_race_after_driver_assignment
- What scenario is being tested: Role change enables race entry.
- Which modules are involved: Crew Management, Race Management, Registration.
- The expected result: Entry succeeds after assigning role to driver.
- The actual result after testing: Passed. Entrant was accepted.
- Any errors or logical issues found: None.

#### TC-IT-03: member_can_satisfy_strategist_mission_after_role_change
- What scenario is being tested: Role change enables mission required-role validation.
- Which modules are involved: Crew Management, Mission Planning, Registration.
- The expected result: Mission starts once strategist role exists.
- The actual result after testing: Passed. Mission started successfully.
- Any errors or logical issues found: None.

#### TC-IT-04: role_reassignment_updates_role_lists
- What scenario is being tested: Role lists reflect reassignment and remove old role membership.
- Which modules are involved: Crew Management, Registration.
- The expected result: Member appears in new role list and not old role list.
- The actual result after testing: Passed. Role list state matched expected.
- Any errors or logical issues found: None.
