-- ============================================================
-- WHO_Immunisation Database Setup
-- SQL Server – Chạy script này để tạo cấu trúc bảng và dữ liệu mẫu
-- ============================================================

USE WHO_Immunisation;
GO

-- ── Bảng Countries ──────────────────────────────────────────
IF OBJECT_ID('dbo.Countries', 'U') IS NULL
CREATE TABLE Countries (
    country_id       INT           IDENTITY(1,1) PRIMARY KEY,
    country_name     NVARCHAR(120) NOT NULL,
    region           NVARCHAR(100),
    economic_status  NVARCHAR(80),   -- Developed / Developing / Least Developed / Emerging Economy / Economy in Transition
    population       BIGINT
);
GO

-- ── Bảng Diseases ───────────────────────────────────────────
IF OBJECT_ID('dbo.Diseases', 'U') IS NULL
CREATE TABLE Diseases (
    disease_id   INT          IDENTITY(1,1) PRIMARY KEY,
    disease_name NVARCHAR(80) NOT NULL UNIQUE   -- e.g. 'Measles', 'Polio', 'Rubella'
);
GO

-- ── Bảng InfectionData ──────────────────────────────────────
IF OBJECT_ID('dbo.InfectionData', 'U') IS NULL
CREATE TABLE InfectionData (
    record_id   INT    IDENTITY(1,1) PRIMARY KEY,
    country_id  INT    NOT NULL REFERENCES Countries(country_id),
    disease_id  INT    NOT NULL REFERENCES Diseases(disease_id),
    year        INT    NOT NULL,
    total_cases BIGINT           -- raw reported cases (NULL if missing)
);
GO

-- ── Bảng Personas (Level 1 - Sub-Task B) ────────────────────
IF OBJECT_ID('dbo.Personas', 'U') IS NULL
CREATE TABLE Personas (
    persona_id  INT           IDENTITY(1,1) PRIMARY KEY,
    name        NVARCHAR(120) NOT NULL,
    role        NVARCHAR(120) NOT NULL,
    organisation NVARCHAR(200),
    description NVARCHAR(500),
    tag1        NVARCHAR(60),
    tag2        NVARCHAR(60),
    icon_color  NVARCHAR(40) DEFAULT 'text-primary'
);
GO

-- ── Bảng TeamMembers (Level 1 - Sub-Task B) ─────────────────
IF OBJECT_ID('dbo.TeamMembers', 'U') IS NULL
CREATE TABLE TeamMembers (
    member_id   INT           IDENTITY(1,1) PRIMARY KEY,
    full_name   NVARCHAR(120) NOT NULL,
    student_id  NVARCHAR(20)  NOT NULL
);
GO

-- ============================================================
-- Dữ liệu mẫu (Sample data – thay thế bằng dữ liệu thực tế)
-- ============================================================

-- Countries
IF NOT EXISTS (SELECT 1 FROM Countries)
BEGIN
    INSERT INTO Countries (country_name, region, economic_status, population) VALUES
    ('Nigeria',         'Africa',       'Developing',           213000000),
    ('Ethiopia',        'Africa',       'Least Developed',      120000000),
    ('DR Congo',        'Africa',       'Least Developed',       95000000),
    ('Pakistan',        'Asia',         'Developing',           225000000),
    ('Chad',            'Africa',       'Least Developed',       17000000),
    ('India',           'Asia',         'Emerging Economy',    1380000000),
    ('Angola',          'Africa',       'Developing',            33000000),
    ('Yemen',           'Middle East',  'Least Developed',       30000000),
    ('Brazil',          'Americas',     'Emerging Economy',     213000000),
    ('China',           'Asia',         'Emerging Economy',    1400000000),
    ('Germany',         'Europe',       'Developed',             83000000),
    ('United States',   'Americas',     'Developed',            330000000),
    ('Japan',           'Asia',         'Developed',            126000000),
    ('Kazakhstan',      'Central Asia', 'Economy in Transition', 19000000),
    ('Tanzania',        'Africa',       'Developing',            59000000),
    ('Afghanistan',     'Asia',         'Least Developed',       39000000),
    ('Mozambique',      'Africa',       'Least Developed',       32000000),
    ('Uganda',          'Africa',       'Least Developed',       46000000);
END
GO

-- Diseases
IF NOT EXISTS (SELECT 1 FROM Diseases)
BEGIN
    INSERT INTO Diseases (disease_name) VALUES
    ('Measles'),
    ('Polio'),
    ('Rubella'),
    ('Tuberculosis'),
    ('Hepatitis B'),
    ('Diphtheria');
END
GO

-- InfectionData (sample rows – replace with actual WHO data)
IF NOT EXISTS (SELECT 1 FROM InfectionData)
BEGIN
    -- Measles 2022 (disease_id=1)
    INSERT INTO InfectionData (country_id, disease_id, year, total_cases) VALUES
    (1,  1, 2022, 18602000),  -- Nigeria
    (2,  1, 2022,  8904000),  -- Ethiopia
    (3,  1, 2022,  6545500),  -- DR Congo
    (4,  1, 2022, 13072500),  -- Pakistan
    (5,  1, 2022,   894200),  -- Chad
    (6,  1, 2022, 59064000),  -- India
    (7,  1, 2022,  1300200),  -- Angola
    (8,  1, 2022,  1101000),  -- Yemen
    (9,  1, 2022,  6708050),  -- Brazil
    (10, 1, 2022, 17220000),  -- China
    (11, 1, 2022,   174300),  -- Germany
    (12, 1, 2022,   594000),  -- United States
    (13, 1, 2022,   113400),  -- Japan
    (14, 1, 2022,  1369800),  -- Kazakhstan
    (15, 1, 2022,  5313100),  -- Tanzania
    (16, 1, 2022,  6401600),  -- Afghanistan
    (17, 1, 2022,  2566400),  -- Mozambique
    (18, 1, 2022,  3220000),  -- Uganda
    -- Rubella 2022 (disease_id=3)
    (1,  3, 2022,  2130000),
    (2,  3, 2022,  1200000),
    (6,  3, 2022,  5520000),
    (11, 3, 2022,    41500),
    (12, 3, 2022,   165000),
    -- Measles 2020 (disease_id=1)
    (1,  1, 2020, 14906000),
    (2,  1, 2020,  7560000),
    (6,  1, 2020, 44022000),
    (9,  1, 2020,  8626650),
    (14, 1, 2020,   758000),
    (16, 1, 2020,  6396000);
END
GO

-- Personas
IF NOT EXISTS (SELECT 1 FROM Personas)
BEGIN
    INSERT INTO Personas (name, role, organisation, description, tag1, tag2, icon_color) VALUES
    ('Dr. Dao Vinh', 'Public Health Researcher', 'Academic / Research',
     'Compare vaccination and infection rates across income groups. Export reliable data for academic reports and publications.',
     'Data Analysis', 'Research', 'text-primary'),
    ('Ms. Do Thi Mai', 'Government Health Policy Advisor', 'Government',
     'Identify high-risk countries or regions quickly to prioritize resource allocation. Understand trends without needing statistical software.',
     'Policy Making', 'Resource Allocation', 'text-orange-500'),
    ('Mr. Le Tung', 'Health Correspondent', 'Media / Communication',
     'Quickly identify key health disparities to build compelling stories. Compare countries against global averages to highlight inequality.',
     'Awareness', 'Benchmarking', 'text-secondary');
END
GO

-- Team Members (thay bằng thông tin nhóm thực tế)
IF NOT EXISTS (SELECT 1 FROM TeamMembers)
BEGIN
    INSERT INTO TeamMembers (full_name, student_id) VALUES
    ('Nguyen Tri Long',  's4224704'),
    ('Dang Quang Nghiem', 's4035375');
END
GO

PRINT 'Database setup complete.';
GO

-- ============================================================
-- Subtask A Tables: Vaccination / Antigen Data
-- ============================================================

IF OBJECT_ID('dbo.Antigens', 'U') IS NULL
CREATE TABLE Antigens (
    antigen_id INT IDENTITY(1,1) PRIMARY KEY,
    antigen_name NVARCHAR(50) NOT NULL UNIQUE
);
GO

IF OBJECT_ID('dbo.VaccinationData', 'U') IS NULL
CREATE TABLE VaccinationData (
    record_id INT IDENTITY(1,1) PRIMARY KEY,
    country_id INT NOT NULL REFERENCES Countries(country_id),
    antigen_id INT NOT NULL REFERENCES Antigens(antigen_id),
    year INT NOT NULL,
    vaccinated_count BIGINT NOT NULL
);
GO

-- Antigen sample data
IF NOT EXISTS (SELECT 1 FROM Antigens)
BEGIN
    INSERT INTO Antigens (antigen_name) VALUES
    ('MCV1'),
    ('MCV2'),
    ('DTP1'),
    ('DTP3'),
    ('POL3');
END
GO

-- Vaccination sample data
-- vaccinated_count is used to calculate vaccination rate:
-- vaccination_rate = vaccinated_count * 100.0 / population
IF NOT EXISTS (SELECT 1 FROM VaccinationData)
BEGIN
    INSERT INTO VaccinationData (country_id, antigen_id, year, vaccinated_count) VALUES
    -- MCV1, 2015
    (1, 1, 2015, 149100000),
    (2, 1, 2015, 72000000),
    (3, 1, 2015, 52250000),
    (4, 1, 2015, 157500000),
    (5, 1, 2015, 9180000),
    (6, 1, 2015, 966000000),
    (7, 1, 2015, 21120000),
    (8, 1, 2015, 17400000),
    (9, 1, 2015, 170400000),
    (10, 1, 2015, 1190000000),
    (11, 1, 2015, 74700000),
    (12, 1, 2015, 280500000),
    (13, 1, 2015, 115920000),
    (14, 1, 2015, 15200000),
    (15, 1, 2015, 36580000),
    (16, 1, 2015, 21060000),
    (17, 1, 2015, 17920000),
    (18, 1, 2015, 25760000),

    -- MCV1, 2022
    (1, 1, 2022, 174660000),
    (2, 1, 2022, 98400000),
    (3, 1, 2022, 76000000),
    (4, 1, 2022, 200250000),
    (5, 1, 2022, 13940000),
    (6, 1, 2022, 1242000000),
    (7, 1, 2022, 29370000),
    (8, 1, 2022, 25500000),
    (9, 1, 2022, 197025000),
    (10, 1, 2022, 1330000000),
    (11, 1, 2022, 80510000),
    (12, 1, 2022, 313500000),
    (13, 1, 2022, 121000000),
    (14, 1, 2022, 18050000),
    (15, 1, 2022, 50150000),
    (16, 1, 2022, 33150000),
    (17, 1, 2022, 27840000),
    (18, 1, 2022, 42320000),

    -- MCV2, 2022
    (1, 2, 2022, 166140000),
    (2, 2, 2022, 94800000),
    (3, 2, 2022, 71250000),
    (4, 2, 2022, 191250000),
    (5, 2, 2022, 13260000),
    (6, 2, 2022, 1200600000),
    (7, 2, 2022, 28050000),
    (8, 2, 2022, 24600000),
    (9, 2, 2022, 193830000),
    (10, 2, 2022, 1316000000),
    (11, 2, 2022, 79680000),
    (12, 2, 2022, 306900000),
    (13, 2, 2022, 119700000),
    (14, 2, 2022, 17860000),
    (15, 2, 2022, 48380000),
    (16, 2, 2022, 31980000),
    (17, 2, 2022, 26880000),
    (18, 2, 2022, 40940000),

    -- DTP3, 2022
    (1, 4, 2022, 170400000),
    (2, 4, 2022, 96000000),
    (3, 4, 2022, 74100000),
    (4, 4, 2022, 195750000),
    (5, 4, 2022, 13600000),
    (6, 4, 2022, 1214400000),
    (7, 4, 2022, 28710000),
    (8, 4, 2022, 25200000),
    (9, 4, 2022, 195960000),
    (10, 4, 2022, 1323000000),
    (11, 4, 2022, 80510000),
    (12, 4, 2022, 310200000),
    (13, 4, 2022, 120960000),
    (14, 4, 2022, 18050000),
    (15, 4, 2022, 49560000),
    (16, 4, 2022, 32760000),
    (17, 4, 2022, 27520000),
    (18, 4, 2022, 41860000);
END
GO

PRINT 'Subtask A vaccination data setup complete.';
GO
