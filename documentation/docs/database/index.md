# DB

## IRS Database structure documenting

The provided SQL schema outlines a database structure designed to support the management and tracking of National Malaria Control Program (NMCP) campaigns such as ITNs, IRS, AMD and other. Here's a detailed description of the database schema based on the revised comments:

### Overview

The schema is organized to facilitate the planning, execution, and reporting of malaria control campaigns. It encompasses various aspects of these campaigns, including:

### Key Components

1. **Campaign Information (`m_campaign`):** This table is central to the schema, categorizing each campaign by type (e.g., IRS or ITNs), year, and other identifying details. It enables the tracking of multiple, simultaneous campaigns.

2. **Locations (`m_villages_locations`):** A comprehensive list of all potential target locations within the country, which can be selected during campaign planning. This table serves as a reference for planning and reporting, without being directly tied to a specific campaign.

3. **Regions (`c_region`):** Specifically for IRS campaigns, regions are defined to streamline planning and resource allocation. Each region can encompass multiple locations and is associated with a specific campaign.

4. **Warehouses/Distribution Points (`c_warehouses_distribution_points`):** Identified locations where campaign materials (pesticides for IRS or nets for ITNs) are stored and from where they are distributed to operational teams. These points are crucial for logistical planning.

5. **Teams (`c_team`):** Details about the teams conducting the spraying or net distribution, including the differentiation between foremen (team leaders) and supervisors for reporting and operational clarity.

6. **Targets (`c_targets_master`):** Planned locations that will be targeted in a certain campaign are stored in this table detailing which the Regions and Wh/distribution points withing each region.

7. **Daily Targets (`c_daily_targets`):** Operational plans detailing which teams are assigned to which targeted-location on specific days, including estimates of population, housing, and the resources required to achieve campaign goals.

8. **Data Collection and Reporting (`c_kobo_irs_team_main`):** Captures detailed reports from the field, including outcomes of daily operations, reasons for any deviations from the plan, and GPS data for verification purposes.

### Purpose and Utility

This schema is designed to support comprehensive tracking and management of NMCP campaigns, facilitating data-driven decision-making and operational efficiency. By structuring data around campaigns, locations, teams, and logistics, the schema provides a solid foundation for monitoring progress, evaluating impact, and planning future campaigns. It allows for detailed reporting and analysis, which are crucial for adjusting strategies, ensuring resource availability, and achieving the overall goal of malaria control and eradication.

### Operational planning

A campaign starts in `campaign_start_date` and takes specified `campaign_days`, Consecutive.

**In planning phase before the campaign:**

- Campaign Start date is determined.
- Locations that will be targeted and sprayed are Specified from `m_villages_locations`.
- Targeted locations are divided and grouped as multiple Regions and within each region into one or more WH-distribution-Point and this info is placed in `c_targets_masters` table.
- the number of required teams are determined and the daily operational plan is planned and `c_daily_targets` table is populated.

**Important variables set during planning:**

- `c_daily_targets.target_houses`: locations total Houses.
- `c_daily_targets.target_room_per_house`: Estimated AVG Rooms per house.
- `c_daily_targets.target_room_avg_area`: a Room Estimated AVG Area.
- `c_daily_targets.target_daily_area_coverage_rate`: Estimated Daily Area coverage Rate per worker.
- `m_campaign.campaign_days`: the Campaign’s number of days `IRS usually planned = 11 days, and ITNs = 6 days`.
- `c_daily_targets.target_area_per_sachet`: Estimated Area Covered per sachet of pesticide is Known `usually = 250`.
- `c_team.team_no_of_team_workers`: number of team's spraying workers.

In the daily Operational plan table A team will cover multiple locations for N-days

**Important calculations:**

- **Estimated Rooms Target** = c_daily_targets.target_houses x c_daily_targets.target_houses.
- **Estimated Area Target** = Estimated Rooms Target x c_daily_targets.target_room_avg_area.
- **Estimated Pesticide sachets Required** = Estimated Area Target / c_daily_targets.target_area_per_sachet.
- Estimated daily area coverage rate per worker = c_kobo_irs_team_main.report_rooms_sprayed_entered x c_daily_targets.target_room_avg_area

**Important meanings and terminology for progress_status:**

When Estimating futures of any thing progress_status is usually need to be taken into account:

- for `progress_status` in  of each sent report:
  - `full`: activity completed in this target with full coverage.
  - `partial`: activity completed in this target with partial coverage.
  - `ongoing`: activity still not completed yet.
  - `NotTargeted, the reason`: activity still not completed yet.

### The Database tables SQL creation

```sql

-- `m_campaign`: Stores information about each campaign. It supports multiple types of campaigns (e.g., ITNs with `campaign_type_id`=1, IRS with `campaign_type_id`=2), allowing the database to track various intervention strategies.

CREATE TABLE 
    m_campaign 
    ( 
        campaign_code         CHARACTER VARYING(64) NOT NULL, 
        campaign_start_date TIMESTAMP(6) WITHOUT TIME ZONE, -- the date the campaign will start
        campaign_days         INTEGER, -- no of campaigns days the campaign is going to take from campaign_start_date.
        campaign_type_id      INTEGER NOT NULL, 
        campaign_id           BIGINT DEFAULT nextval('m_campaign_campaign_serial_seq'::regclass) 
        NOT NULL, 
        campaign_note CHARACTER VARYING(255), 

        PRIMARY KEY (campaign_id), 
        CONSTRAINT campaign_type_fk FOREIGN KEY (campaign_type_id) 
        REFERENCES "m_campaigntypes" ("campaign_type_id"), 
        UNIQUE (campaign_code)
    );

-- `m_villages_locations`: Catalogs potential target locations across the country. Selections for specific campaigns are made during planning and are utilized in tables like `daily_targets` and for reporting in `c_kobo_irs_team_main` and `c_kobo_itns_team_main`.

CREATE TABLE m_villages_locations
(
    location_id                BIGINT DEFAULT nextval('location_id_serial_seq'::regclass) NOT NULL,
    location_district_id     BIGINT NOT NULL,
    location_ppc_code          BIGINT NOT NULL,
    location_subdistrict_name  CHARACTER VARYING(255),
    location_village_name      CHARACTER VARYING(255),
    location_subvillage_name   CHARACTER VARYING(255),
    location_longitude         DOUBLE PRECISION,
    location_latitude          DOUBLE PRECISION,
    CONSTRAINT villages_locations_pkey PRIMARY KEY (location_id),
    CONSTRAINT villages_locations_district_id_fk FOREIGN KEY (location_district_id) 
    REFERENCES "m_districts" ("district_id"),
    CONSTRAINT villages_locations_ppc_code_ux UNIQUE (location_ppc_code)
);

-- `c_region`: Defines regions for IRS campaigns, where each encompasses multiple locations. These regions are used for logistical planning, including warehouse/distribution point assignments and team management. The structure supports nested regions through warehouse and team assignments. For IRS campaigns only, regions are defined in this table, each linked to a specific campaign.

CREATE TABLE c_region
(
    region_id          BIGINT DEFAULT nextval('c_region_serial_seq'::regclass) NOT NULL,
    region_name        CHARACTER VARYING(255),
    region_head        CHARACTER VARYING(255),
    region_notes       CHARACTER VARYING(255),
    region_campaign_id BIGINT NOT NULL,
    region_name_en     CHARACTER VARYING(255),
    region_number      INTEGER NOT NULL,
    PRIMARY KEY (region_id),
    CONSTRAINT c_region_campaign_id_fk FOREIGN KEY (region_campaign_id) 
    REFERENCES "m_campaign" ("campaign_id")
);

-- `c_warehouses_distribution_points`: Lists distribution points for both ITNs and IRS campaigns, indicating where resources are staged for distribution to teams. ITNs campaigns do not use regional divisions, hence `wh_region_id` can be null for them.

CREATE TABLE c_warehouses_distribution_points
(
    wh_id              BIGINT DEFAULT nextval('c_warehouses_serial_seq'::regclass) NOT NULL,
    wh_name            CHARACTER VARYING(255),
    wh_description     CHARACTER VARYING(255),
    wh_gps_coordinate  CHARACTER VARYING(255),
    wh_campaign_id     BIGINT,
    wh_region_id       BIGINT,
    CONSTRAINT c_warehouses_pkey PRIMARY KEY (wh_id),
    CONSTRAINT wh_campaign_id_fk FOREIGN KEY (wh_campaign_id) 
    REFERENCES "m_campaign" ("campaign_id"),
    CONSTRAINT wh_region_id_fk FOREIGN KEY (wh_region_id) 
    REFERENCES "c_region" ("region_id")
);

-- `c_team`: Represents teams tasked with either spraying (IRS), including team leaders and supervisors. The crucial team_type field differentiates between foreman teams directly involved in spraying and supervisor teams overseeing multiple foreman teams and consolidating their reports. it has either [FOREMAN, SUPERVISOR].

CREATE TABLE c_team
(
    team_id            BIGINT DEFAULT nextval('c_team_new_serial_seq'::regclass) NOT NULL,
    team_contact_person TEXT,
    team_wh_id         BIGINT NOT NULL,
    team_number        BIGINT NOT NULL,
    team_type          team_type, 
    team_no_of_team_workers   INTEGER, -- Team No of workers
    CONSTRAINT c_team_new_pkey PRIMARY KEY (team_id),
    CONSTRAINT c_team_wh_id_fk FOREIGN KEY (team_wh_id) 
    REFERENCES "c_warehouses_distribution_points" ("wh_id")
);

-- `c_targets_master`: 
    
-- `c_daily_teams_targets`: 
-- This table defines the operational plan for each day within an IRS campaign.
-- Key points:
-- * Estimated values based on planning, actual execution details in `c_kobo_irs_team_main`.
-- * Divergences from planned teams/dates captured in `c_kobo_irs_team_main`.
-- * Multiple reports per target on different days possible in `c_kobo_irs_team_main`.
-- * Progress tracking: Latest report's progress_status is considered for progress tracking.

-- Fields:

-- * target_team_id: The team assigned to the target for this day. (FK to c_team)
-- * target_day_date_id: The date ID for the planned spraying day. (FK to m_date_dimension)
-- * target_population (optional): Estimated population of the target location.
-- * target_houses: Estimated number of houses in the target location.
-- * target_room_per_house: Estimated number of rooms per house in the target location.
-- * target_room_avg_area: Estimated area per room.
--     Used to estimate total area requiring insecticide coverage.
-- * target_daily_area_coverage_rate: Estimated daily area coverage rate per worker.
--     in a day. Used to assess workload and monitor progress.
-- target_area_per_sachet: Estimated Area covered Per Sachet.

CREATE TABLE 
    c_daily_teams_targets 
    ( 
        target_id   BIGINT DEFAULT nextval('c_daily_team_targets_target_id_seq'::regclass) NOT NULL, 
        target_warehouse_id BIGINT NOT NULL, 
        target_location_id  BIGINT NOT NULL, 
        target_region_id    BIGINT, 
        target_field_code   BIGINT NOT NULL, 
        target_team_id      BIGINT NOT NULL, 
        target_day_date_id  INTEGER NOT NULL, 
        target_population DOUBLE PRECISION, 
        target_houses DOUBLE PRECISION, 
        target_room_per_house           NUMERIC, 
        target_room_avg_area            NUMERIC, 
        target_daily_area_coverage_rate INTEGER, 
        target_area_per_sachet          INTEGER, 
        location_longitude DOUBLE PRECISION, 
        location_latitude DOUBLE PRECISION, 
        target_campaign_id BIGINT, 
        PRIMARY KEY (target_id), 
        CONSTRAINT fk_target_location_id FOREIGN KEY (target_location_id) REFERENCES 
        "m_villages_locations" ("location_id"), 
        CONSTRAINT fk_target_region_id FOREIGN KEY (target_region_id) REFERENCES "c_region" 
        ("region_id"), 
        CONSTRAINT fk_target_warehouse_id FOREIGN KEY (target_warehouse_id) REFERENCES 
        "c_warehouses_distribution_points" ("wh_id"), 
        CONSTRAINT fk_target_team_id FOREIGN KEY (target_team_id) REFERENCES "c_team" ("team_id"), 
        CONSTRAINT fk_target_day_date_id FOREIGN KEY (target_day_date_id) REFERENCES 
        "m_date_dimension" ("date_id"), 
        CONSTRAINT fk_target_campaign_id FOREIGN KEY (target_campaign_id) REFERENCES "m_campaign" 
        ("campaign_id"), 
        UNIQUE (target_id), 
        CONSTRAINT c_daily_teams_wh_code_team_day_multiple_u UNIQUE (target_warehouse_id, 
        target_team_id, target_day_date_id, target_field_code), 
        CONSTRAINT c_daily_teams_camp_code_team_day_multiple_u UNIQUE (target_field_code, 
        target_team_id, target_day_date_id, target_campaign_id) 
    );

-- `c_kobo_irs_team_main`:
-- This table captures detailed field reports submitted by spray teams during IRS campaigns.
-- It provides granular data on sprayed households, insecticide usage, and coverage per house.

-- Fields:

-- * _id: Unique identifier for the report.
-- * _uuid: Unique identifier for the data submission.
-- * _submission_time: Timestamp when the report was submitted.
-- * progress_status: One of "full", "ongoing", "partial", "rejected", "displaced", "war_zone", or "non_sprayed_for_reason".
-- * report_unspray_reason (optional): Reason for non-spraying if
--     progress_status is "non_sprayed_for_reason".
-- * report_completeness_note: comment for any progress_status chosen coverage.
-- * report_tl_comment: team leader other comments.
-- * target_id: FK to the target location in `c_targets_master`.
-- * report_team_id: The team that covered the location and submitted the report.
--     (FK to c_team)
-- * day_date_id: The date the spraying occurred.
-- * report_houses_total_entered: Total number of houses visited.
-- * report_houses_sprayed_entered: Number of houses sprayed out of total visited.
-- * report_houses_nonsprayed_entered: Number of houses not sprayed out of total visited.
-- * report_houses_refused_entered: Number of houses that refused spraying.
-- * report_houses_closed_entered: Number of houses that were closed.
-- * report_population_in_sprayed_entered: Estimated population in sprayed houses.
-- * report_rooms_total_entered: Total number of rooms in visited houses.
-- * report_rooms_sprayed_: Total number of rooms sprayed from total rooms.
-- * report_rooms_nonsprayed_entered: Total number of rooms non-sprayed from total rooms.
-- * report_total_sachets_entered: pesticides sachets consumed.

CREATE TABLE c_kobo_irs_team_main
(
    _id                           BIGINT NOT NULL,
    _uuid                         CHARACTER VARYING(255) NOT NULL,
    _submission_time              TIMESTAMP(6) WITHOUT TIME ZONE, 
    progress_status               CHARACTER VARYING(255) NOT NULL,
    report_unspray_reason         CHARACTER VARYING(2000),
    report_tl_comment         CHARACTER VARYING(2000),
    report_other_unspray_reason         CHARACTER VARYING(2000),
    report_reason_not_return         CHARACTER VARYING(2000),
    report_completeness_note         CHARACTER VARYING(2000),
    target_id                   BIGINT NOT NULL,
    report_team_id            BIGINT NOT NULL, 
    day_date_id                   INTEGER NOT NULL,
    report_houses_total_entered   INTEGER,
    report_houses_sprayed_entered INTEGER,
    report_houses_nonsprayed_entered INTEGER, 
    report_houses_refused_entered INTEGER, 
    report_houses_closed_entered  INTEGER,
    report_population_in_sprayed_entered INTEGER,
    report_rooms_total_entered    INTEGER, 
    report_rooms_sprayed_entered  INTEGER, 
    report_rooms_nonsprayed_entered INTEGER, 
    report_total_sachets_entered  INTEGER, 
    report_captured_gps           CHARACTER VARYING(255), 
    _database_created_at          TIMESTAMP(6) WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT c_kobo_irs_team_main_2_pkey PRIMARY KEY (_id),
    CONSTRAINT c_irs_kobo2_day_date_id_fk FOREIGN KEY (day_date_id) REFERENCES "m_date_dimension" ("date_id"),
    CONSTRAINT c_irs_kobo2_target_id_fk FOREIGN KEY (target_id) REFERENCES "c_daily_teams_targets" ("target_id"),
    CONSTRAINT c_irs_kobo2_team_id_fk FOREIGN KEY (report_team_id) REFERENCES "c_team" ("team_id"),
    CONSTRAINT c_irs_kobo_kobo2_uuid_u UNIQUE (_uuid)
);

-- Note: This is the crucial tables, additional tables are implied but not listed here for brevity.
```
