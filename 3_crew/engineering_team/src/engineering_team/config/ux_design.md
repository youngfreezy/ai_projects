# Trading Simulation Platform - UX Design Specification

## Overview
A modern, professional React/Redux web application for simulating trading operations with a beautiful, intuitive user interface.

## Visual Design

### Color Scheme
- **Primary Gradient**: Purple to violet (135deg, #667eea 0%, #764ba2 100%)
- **Success Gradient**: Teal to green (135deg, #11998e 0%, #38ef7d 100%)
- **Danger Gradient**: Pink to red (135deg, #f093fb 0%, #f5576c 100%)
- **Warning Gradient**: Pink to yellow (135deg, #fa709a 0%, #fee140 100%)
- **Background**: Full-screen gradient (purple theme)
- **Cards**: White with subtle shadows and rounded corners

### Typography
- **Font Family**: System fonts (-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', etc.)
- **Headings**: Bold, colored with primary theme (purple)
- **Body Text**: Clean, readable sans-serif
- **Main Title**: 48px, bold, white, centered

### Layout Components

#### Cards
- White background
- 15px border-radius
- 30px padding
- Box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2)
- No border

#### Tabs
- Custom styled tabs (not default Bootstrap)
- Background: rgba(255, 255, 255, 0.1) when inactive
- Background: white when active
- Text: white when inactive, purple when active
- 10px border-radius
- 15px vertical padding, 30px horizontal padding
- Hover effect: slight lift (translateY(-2px))
- Transition animations on all interactions

#### Form Inputs
- Border: 2px solid #e0e0e0
- 8px border-radius
- 12px vertical padding, 15px horizontal padding
- Focus state: purple border (#667eea) with subtle shadow
- Labels: bold, 600 weight, dark gray (#333)

#### Buttons
- Multiple gradient styles (primary, success, danger, warning)
- 12px vertical padding, 30px horizontal padding
- 8px border-radius
- Font weight: 600
- Hover effects: lift (translateY(-2px)) + shadow
- Smooth transitions (0.3s ease)

#### Information Displays
- Account Info boxes: gradient background with subtle purple tint
- Border: 2px solid with rgba opacity for theme colors
- 12px border-radius, 20px padding
- 18px font size for values

#### Lists
- No default bullets
- Each item styled as a card
- Left border accent (4px solid #667eea)
- White background
- 15px padding, 10px bottom margin
- Rounded corners (8px)
- Subtle shadow

## Component Structure

### Main App (App.jsx)
- Centered max-width container (1200px)
- 20px padding
- White centered title (48px, bold)

### Tab Navigation
- Account Management
- Trading
- Reports

### Account Management Tab
- Two-column layout (responsive)
- Left column: form inputs and action buttons
- Right column: account information display
- Operation results displayed below buttons
- Real-time updates

### Trading Tab
- Two-column layout (responsive)
- Left column: symbol and quantity inputs with buy/sell buttons
- Right column: current stock prices reference panel
- Operation results for trade confirmations

### Reports Tab
- Two-column layout for portfolio metrics
- Portfolio Value: large (32px), bold, teal/green
- Profit/Loss: large (32px), bold, conditional color (green for profit, red for loss)
- Holdings: list format
- Transaction History: full-width below metrics
- Empty states handled gracefully

## Interactions & Animations

### Hover States
- Buttons: translateY(-2px) + enhanced shadow
- Tabs: background opacity increase
- Smooth transitions (0.3s ease)

### Focus States
- Inputs: purple border + subtle purple shadow
- Keyboard accessibility maintained

### Responsive Design
- Breakpoint: 768px
- Mobile: single column layout
- Buttons: full width on mobile
- Padding reduced on smaller screens
- Tab font size adjusts for mobile

## Technical Requirements

### Dependencies
- react-bootstrap: ^2.10.0
- bootstrap: ^5.3.2
- Bootstrap CSS imported in index.js
- Custom CSS in index.css and App.css

### Bootstrap Components Used
- Container, Row, Col (layout)
- Form, Form.Group, Form.Control, Form.Label
- Button
- Tabs, Tab

### Custom CSS Classes
- `.App` - main container
- `.card` - card styling
- `.account-info` - information display boxes
- `.operation-result` - result messages
- `.btn-{color}` - custom button gradients

## Accessibility
- Semantic HTML structure
- Proper form labels
- ARIA attributes where needed
- Keyboard navigation support
- High contrast text
- Focus indicators

## Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers supported
- Responsive design works on all screen sizes

## File Structure
```
src/
├── App.jsx (import Bootstrap Tabs)
├── App.css (component styling)
├── index.js (import Bootstrap CSS)
├── index.css (global styles)
├── components/
│   ├── AccountManagement.jsx (Bootstrap Form components)
│   ├── Trading.jsx (Bootstrap Form components)
│   ├── Reports.jsx (Bootstrap layout components)
│   ├── AccountInfo.jsx
│   └── OperationResult.jsx
└── store/
    └── accountSlice.js
```

## Implementation Notes
- All styling must be applied via CSS files, not inline styles (except specific dynamic colors)
- Bootstrap provides the base, custom CSS enhances the design
- Gradient backgrounds and buttons create modern, professional appearance
- Consistent spacing and padding throughout
- Smooth transitions enhance user experience
- Cards create visual hierarchy and content separation

