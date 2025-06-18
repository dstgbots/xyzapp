# GetBandish: Classical Indian Music Composition Management System
## A Mobile Application Development Project

**Project Report**

---

**Submitted by:** K Kousthubh Bhat  
**Course:** BCA 2nd Year  
**Project Duration:** April 27 - June 19, 2024 (54 days)  
**Technology Stack:** Python, Kivy, KivyMD, SQLite  
**Version:** 2.0 (SQLite Edition)  

---

## Table of Contents

1. **Executive Summary & Introduction**
2. **Research & Background Study**
3. **System Design & Architecture**
4. **Implementation & Development**
5. **Testing, Deployment & Future Scope**

---

## 1. Executive Summary & Introduction

### 1.1 Project Overview

GetBandish is a modern mobile application designed to preserve, organize, and manage classical Indian music compositions (bandish) and musical scales (raagas). The application serves as a comprehensive digital library for Indian classical music enthusiasts, students, and practitioners, providing easy access to traditional compositions with their complete lyrics, taal (rhythm), and raaga information.

### 1.2 Problem Statement

Traditional Indian classical music faces several challenges in the digital age:
- **Preservation Crisis**: Ancient compositions are stored in fragmented physical manuscripts
- **Accessibility Issues**: Limited digital resources for classical music students and practitioners
- **Organization Challenges**: Lack of systematic categorization and searchable databases
- **Learning Barriers**: Difficulty in accessing authentic lyrics and composition details
- **Concert Planning**: No digital tools for organizing classical music performances

### 1.3 Objectives

**Primary Objectives:**
- Create a comprehensive digital repository of Indian classical music compositions
- Develop an intuitive mobile-first user interface for easy navigation
- Implement robust search and categorization functionality
- Enable users to create and manage custom concert playlists
- Provide offline functionality for uninterrupted access

**Secondary Objectives:**
- Promote cultural preservation through digital documentation
- Support music education with detailed composition information
- Enable collaborative music curation through admin controls
- Demonstrate modern software development practices for academic assessment

### 1.4 Scope & Limitations

**Project Scope:**
- Database of 15+ classical raagas with detailed compositions
- Complete lyrics and metadata for 50+ bandish compositions
- Cross-platform mobile application (Android primary)
- Administrative tools for database management
- Concert planning and custom composition features

**Current Limitations:**
- Audio playback functionality not implemented
- Limited to text-based compositions (no notation support)
- Single-user system (no cloud synchronization)
- Focused on Hindustani classical music tradition

---

## 2. Research & Background Study

### 2.1 Indian Classical Music: Cultural Context

Indian classical music represents one of the world's oldest continuous musical traditions, with origins tracing back over 3,000 years. The system is built around two fundamental concepts:

**Raaga (राग):** A melodic framework consisting of specific note combinations that evoke particular emotions and are associated with specific times of day or seasons. Examples include:
- *Abhogi*: A pentatonic raaga known for its devotional character
- *Asavari*: A morning raaga with serious, contemplative mood
- *Bageshree*: A late-night raaga expressing longing and romance

**Taal (ताल):** Rhythmic cycles that provide the temporal framework for compositions. Common taals include:
- *Teen Taal*: 16-beat cycle (most common)
- *Ek Taal*: 12-beat cycle
- *Jhap Taal*: 10-beat cycle

**Bandish (बंदिश):** Fixed compositions that combine raaga (melody), taal (rhythm), and sahitya (lyrics), serving as the foundation for improvisation in classical performances.

### 2.2 Technology Research & Selection

#### 2.2.1 Framework Evaluation

**Initial Choice: Tkinter (April 27 - June 16, 2024)**
- *Advantages*: Simple Python integration, familiar from coursework
- *Limitations*: Limited mobile support, outdated UI components, poor cross-platform compatibility
- *Decision*: Migrated to Kivy for mobile development capabilities

**Final Choice: Kivy + KivyMD (June 17 - June 19, 2024)**
- *Kivy Framework*: Cross-platform Python framework supporting mobile deployment
- *KivyMD*: Material Design components providing modern, professional UI elements
- *Advantages*: True mobile development, beautiful UI components, single codebase for multiple platforms

#### 2.2.2 Database Architecture Research

**SQLite Selection Rationale:**
- **Embedded Database**: No server requirements, perfect for mobile applications
- **ACID Compliance**: Ensures data integrity for music composition storage
- **Cross-Platform**: Works seamlessly across Windows, Android, and iOS
- **Performance**: Optimized for read-heavy operations typical in music browsing applications
- **File-Based**: Easy backup and distribution of complete music libraries

### 2.3 Competitive Analysis

**Existing Solutions Analysis:**

1. **Traditional Methods:**
   - Physical songbooks and manuscripts
   - *Limitations*: Not searchable, difficult to organize, prone to damage

2. **Digital Platforms:**
   - General music streaming services (Spotify, YouTube)
   - *Limitations*: Focus on popular music, poor classical music categorization, no lyrics/composition details

3. **Specialized Classical Music Apps:**
   - Limited offerings for Indian classical music
   - Most focus on Western classical music or lack comprehensive composition databases

**Market Gap Identified:** No comprehensive mobile application specifically designed for Indian classical music composition management with offline capabilities and detailed metadata.

### 2.4 User Requirements Analysis

**Primary User Groups:**
1. **Classical Music Students**: Need easy access to composition lyrics and technical details
2. **Performing Artists**: Require concert planning tools and repertoire management
3. **Music Teachers**: Need organized curriculum materials and reference resources
4. **Cultural Researchers**: Require systematic documentation and search capabilities

**Functional Requirements Derived:**
- Intuitive browsing by raaga or composition type
- Advanced search capabilities across all metadata fields
- Favorite/wishlist functionality for personal curation
- Concert playlist creation and management
- Administrative tools for content management

---

## 3. System Design & Architecture

### 3.1 Application Architecture

**Model-View-Controller (MVC) Pattern Implementation:**

```
GetBandish Application Architecture

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     View        │    │   Controller    │    │     Model       │
│   (KivyMD UI)   │◄──►│  (main.py)      │◄──►│  (database.py)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        ▲                       ▲                       ▲
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Screen Classes  │    │ Event Handlers  │    │ SQLite Database │
│ • WelcomeScreen │    │ • Navigation    │    │ • getbandish.db │
│ • MainScreen    │    │ • Search        │    │ • Tables:       │
│ • BandishList   │    │ • CRUD Ops      │    │   - raagas      │
│ • DetailScreen  │    │ • User Actions  │    │   - bandish     │
│ • AdminPanel    │    │                 │    │   - concerts    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 3.2 Database Schema Design

**Entity Relationship Model:**

```sql
-- Raagas Table (Musical Scales)
CREATE TABLE raagas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    is_active INTEGER DEFAULT 0,        -- Available for browsing
    is_favorite INTEGER DEFAULT 0,      -- User wishlist
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bandish Table (Compositions)
CREATE TABLE bandish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    raaga_id INTEGER,                   -- Foreign Key to raagas
    taal TEXT NOT NULL,                 -- Rhythm cycle
    type TEXT NOT NULL,                 -- Composition type
    lyrics TEXT NOT NULL,               -- Complete composition text
    is_favorite INTEGER DEFAULT 0,      -- User wishlist
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (raaga_id) REFERENCES raagas (id)
);

-- Concerts Table (User Playlists)
CREATE TABLE concerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    user_id TEXT DEFAULT 'default_user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.3 User Interface Design

**Material Design Implementation:**

- **Color Scheme**: Traditional Indian classical music theme
  - Primary: `#8B4513` (Saddle Brown) - representing classical instruments
  - Secondary: `#D4AF37` (Gold) - symbolic of traditional ornamentation
  - Background: `#FFF8DC` (Cornsilk) - resembling manuscript paper

- **Navigation Structure**:
  - **Drawer Navigation**: Slide-out menu for major functions
  - **Tab-Based Search**: Separate tabs for raaga and bandish search
  - **Card-Based Display**: Each composition presented in Material Design cards
  - **Floating Action Buttons**: For primary actions (favorites, search)

### 3.4 Mobile Development Strategy

**Cross-Platform Deployment:**

1. **Android Primary Target**:
   - Buildozer configuration for APK generation
   - Minimum SDK: Android 7.0 (API 24)
   - Target SDK: Android 12 (API 31)
   - Architecture: ARM64 + ARMv7 for broad device compatibility

2. **Build Process**:
   - Local development on Windows/Linux
   - Cloud building via Google Colab for accessibility
   - Automated build scripts for streamlined deployment

---

## 4. Implementation & Development

### 4.1 Development Methodology

**Iterative Development Approach (54-day timeline):**

**Phase 1: Foundation (Days 1-15)**
- Technology research and selection (Tkinter evaluation)
- Basic UI framework and welcome screen implementation
- Core navigation structure development

**Phase 2: Core Features (Days 16-35)**
- Database integration and data modeling
- Main browsing functionality (raaga → bandish navigation)
- Detailed composition viewing with lyrics display

**Phase 3: Advanced Features (Days 36-45)**
- Search functionality implementation
- User preference system (favorites/wishlist)
- Administrative tools for content management

**Phase 4: Mobile Optimization (Days 46-54)**
- Migration from Tkinter to KivyMD
- Mobile UI redesign with Material Design
- Android build system implementation

### 4.2 Key Technical Implementations

#### 4.2.1 Dynamic Screen Management

The application uses KivyMD's screen manager for seamless navigation between different app sections. Each screen is implemented as a separate class inheriting from MDScreen, promoting modularity and maintainability.

#### 4.2.2 Database Abstraction Layer

A comprehensive DatabaseManager class handles all SQLite operations, providing methods for:
- CRUD operations on raagas and bandish
- Advanced search functionality
- User preference management
- Concert playlist operations
- Data integrity maintenance

### 4.3 User Experience Enhancements

#### 4.3.1 Progressive Loading
- Welcome screen with 3-second loading animation
- Lazy loading of composition details to improve performance
- Smooth transitions between screens using KivyMD animations

#### 4.3.2 Search Implementation
- Real-time search across composition titles and lyrics
- Separate search tabs for raagas and bandish
- Filter integration with user favorites

#### 4.3.3 Responsive Design
- Adaptive layouts for different screen sizes
- Dynamic text sizing based on content length
- Touch-optimized interface elements

### 4.4 Data Management Strategy

**Initial Data Population:**
- 15 classical raagas with comprehensive metadata
- 50+ traditional bandish compositions
- Complete lyrics in Devanagari transliteration
- Technical details (taal, composition type, raaga association)

**Content Curation Process:**
1. Research traditional compositions from authentic sources
2. Verify lyrics and technical details with classical music references
3. Standardize transliteration for consistency
4. Implement quality control through administrative interface

---

## 5. Testing, Deployment & Future Scope

### 5.1 Testing Strategy

#### 5.1.1 Functional Testing
**Core Feature Validation:**
- Navigation flow testing across all screens
- Database CRUD operations verification
- Search functionality accuracy testing
- User preference persistence validation

**Test Cases Executed:**
- Raaga to Bandish navigation workflow
- Favorite system toggle and persistence
- Concert creation and management
- Administrative panel functionality
- Cross-platform compatibility

#### 5.1.2 Performance Testing
- Database query optimization for large datasets
- Memory usage monitoring during extended browsing sessions
- Application startup time measurement
- Smooth scrolling validation for long composition lists

### 5.2 Deployment Architecture

#### 5.2.1 Build Configuration

**Buildozer Specification:**
- Package name: org.kousthubh.getbandish
- Requirements: Python3, Kivy 2.2.0, KivyMD 1.1.1, SQLite3
- Permissions: Internet, Storage access
- Target Android API: 31
- Architecture: Universal (ARM64 + ARMv7)

#### 5.2.2 Distribution Strategy

**Multiple Build Options:**
1. **Google Colab Build**: Cloud-based building for accessibility
2. **Local Linux Build**: For developers with Linux environments
3. **GitHub Actions**: Automated build pipeline for continuous deployment

**APK Specifications:**
- Size: 15-25 MB (including database)
- Minimum Android Version: 7.0 (API 24)
- Offline Functionality: Complete database embedded in APK

### 5.3 Project Outcomes & Metrics

#### 5.3.1 Technical Achievements
- **Codebase**: 3,800+ lines of Python code
- **Database**: 5 normalized tables with referential integrity
- **UI Components**: 10+ custom screen classes with Material Design
- **Features**: 15+ major features including search, favorites, concert management

#### 5.3.2 Learning Outcomes
- **Mobile Development**: Gained expertise in cross-platform mobile app development
- **Database Design**: Implemented normalized relational database with complex queries
- **UI/UX Design**: Applied Material Design principles for professional interfaces
- **Software Engineering**: Practiced version control, documentation, and testing methodologies

### 5.4 Future Enhancement Roadmap

#### 5.4.1 Short-term Enhancements (3-6 months)
**Audio Integration:**
- MP3 playback functionality for composition audio
- Recording capability for custom compositions
- Audio visualization during playback

**Enhanced Search:**
- Voice search integration
- Advanced filtering by taal, composer, era
- Fuzzy search for handling transliteration variations

**Social Features:**
- User accounts and cloud synchronization
- Composition sharing between users
- Community ratings and reviews

#### 5.4.2 Long-term Vision (6-12 months)
**Artificial Intelligence Integration:**
- Automatic raaga identification from hummed melodies
- Composition recommendation based on user preferences
- Natural language processing for lyric analysis

**Educational Features:**
- Interactive raaga learning modules
- Taal practice with metronome integration
- Notation display alongside text lyrics

**Platform Expansion:**
- iOS application development
- Web-based version for desktop access
- Smart TV application for large-screen viewing

**Cultural Preservation:**
- Collaboration with music institutions for content expansion
- Historical context and composer biography integration
- Regional variation documentation (Carnatic music support)

### 5.5 Conclusion

The GetBandish project successfully demonstrates the intersection of traditional cultural preservation and modern software development. Through iterative development and user-centered design, the application provides a comprehensive solution for Indian classical music composition management.

**Key Success Factors:**
1. **Technical Excellence**: Robust architecture supporting scalability and maintainability
2. **Cultural Sensitivity**: Authentic representation of classical music traditions
3. **User Experience**: Intuitive interface design facilitating easy music discovery
4. **Educational Value**: Comprehensive documentation serving as learning resource

The project not only fulfills academic requirements but also contributes meaningfully to cultural preservation efforts, providing a foundation for continued development and community engagement in the classical music domain.

**Final Metrics:**
- **Development Duration**: 54 days
- **Code Quality**: Well-documented, modular architecture
- **User Interface**: Professional Material Design implementation
- **Database**: Comprehensive music composition repository
- **Deployment**: Cross-platform mobile application ready for distribution

This project represents a significant achievement in combining technical skills with cultural appreciation, demonstrating the potential for technology to serve traditional arts and education. 