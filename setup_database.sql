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
