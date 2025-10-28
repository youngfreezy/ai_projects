# Frontend Architecture Design

This document outlines the complete technical architecture for implementing a React/Redux trading simulation application.

## Project Structure

```
output/react_app/
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   ├── index.css
│   ├── App.jsx
│   ├── App.css
│   ├── components/
│   │   ├── AccountManagement.jsx
│   │   ├── Trading.jsx
│   │   ├── Reports.jsx
│   │   ├── AccountInfo.jsx
│   │   └── OperationResult.jsx
│   ├── store/
│   │   ├── index.js
│   │   └── slices/
│   │       └── accountSlice.js
│   └── api/
│       └── backend.js
└── package.json
```

## Dependencies

### package.json
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "redux": "^4.2.1",
    "react-redux": "^8.1.3",
    "@reduxjs/toolkit": "^1.9.7",
    "axios": "^1.6.2",
    "react-bootstrap": "^2.10.0",
    "bootstrap": "^5.3.2"
  }
}
```

## File Specifications

### public/index.html
- Standard HTML5 document structure
- Viewport meta tag for responsive design
- Title: "Trading Simulation Platform"
- div#root container for React mounting

### src/index.js
- Import Bootstrap CSS: `import 'bootstrap/dist/css/bootstrap.min.css'`
- Import index.css for global styles
- React 18 createRoot API
- Redux Provider wrapping App component
- Render to #root element

### src/index.css
- Global resets and base styles
- Gradient background (purple to violet)
- System font stack
- Body min-height 100vh

### src/App.jsx
- Import React, Bootstrap Tabs/Tab components
- Import App.css
- Import all three tab components
- Container with max-width 1200px, centered
- Styled title header (white, 48px, centered)
- Three-tab navigation: Account Management, Trading, Reports

### src/App.css
- Custom tab styling (gradient backgrounds, hover effects)
- Card component styling (white, shadow, rounded corners)
- Button styling (gradient backgrounds, hover lift effects)
- Form input styling (border, focus states)
- Account info display styling
- Operation result styling
- Responsive breakpoints (768px)

### Components

#### AccountManagement.jsx
- Container/Row/Col Bootstrap layout
- Two-column layout (responsive)
- Form.Group with Form.Control for amount input
- Three buttons: Create Account (success), Deposit (primary), Withdraw (danger)
- OperationResult component for feedback
- AccountInfo component in right column

#### Trading.jsx
- Container/Row/Col Bootstrap layout
- Two-column layout (responsive)
- Two Form.Controls: Symbol (text) and Quantity (number)
- Two buttons: Buy Shares (success), Sell Shares (danger)
- OperationResult component
- Current stock prices reference panel in right column

#### Reports.jsx
- Container/Row/Col Bootstrap layout
- Portfolio Value display (large, teal/green color)
- Profit/Loss display (large, conditional color: green/red)
- Holdings list (styled list items)
- Transaction history list (styled list items)
- Empty state handling

#### AccountInfo.jsx
- Uses useSelector to get balance and holdings from Redux
- Displays balance with formatting
- Displays holdings as list items
- Empty state for no holdings

#### OperationResult.jsx
- Conditional rendering (null if no message)
- Formatted message display with styling

### Redux Architecture

#### src/store/index.js
- Import configureStore from @reduxjs/toolkit
- Import accountReducer from accountSlice
- Export store with account reducer
- Export RootState and AppDispatch types

#### src/store/slices/accountSlice.js
- Import createSlice from @reduxjs/toolkit
- Initial state: { user_id: null, balance: 0, holdings: {}, transactions: [], portfolioValue: 0, profitOrLoss: 0 }
- Reducers:
  - createAccount: Sets user data and initial balance
  - deposit: Adds to balance, adds transaction
  - withdraw: Subtracts from balance, adds transaction
  - buyShares: Calculates cost, updates balance and holdings, adds transaction
  - sellShares: Calculates revenue, updates balance and holdings, adds transaction
  - calculatePortfolioValue: Sums balance and holdings value
  - calculateProfitOrLoss: Portfolio value minus initial deposit
- Thunks for async operations if needed
- Selectors for computed values

### API Integration

#### src/api/backend.js
- Import axios
- **CRITICAL**: Create axios instance with baseURL: https://huggingface.co/spaces/fareezaiahmed/trading-app-api
- **DO NOT use localhost or any other URL**
- Export API methods:
  - createAccount(initialDeposit)
  - deposit(amount)
  - withdraw(amount)
  - buyShares(symbol, quantity)
  - sellShares(symbol, quantity)
  - getPortfolio()
- All methods use async/await
- Error handling with try/catch
- Returns JSON responses

## Implementation Patterns

### Component Pattern
- All components use functional components with hooks
- PropTypes for type checking (optional)
- Destructure props for cleaner code
- Use React.memo for performance if needed

### Redux Pattern
- Use hooks: useSelector, useDispatch
- Store account state in Redux store
- All business logic in reducers
- UI components dispatch actions
- Components read state via selectors

### Styling Pattern
- Bootstrap for layout and base components
- Custom CSS for design specifications
- Inline styles only for dynamic colors
- CSS variables for theme colors
- Mobile-first responsive design

### API Pattern
- Axios for HTTP requests
- Async/await for async operations
- Error boundaries for error handling
- Loading states for async operations

## File Creation Implementation

### Directory Setup
- Use Code Interpreter to create directory structure first:
  ```python
  import os
  os.makedirs('output/react_app', exist_ok=True)
  os.makedirs('output/react_app/public', exist_ok=True)
  os.makedirs('output/react_app/src', exist_ok=True)
  os.makedirs('output/react_app/src/components', exist_ok=True)
  os.makedirs('output/react_app/src/store', exist_ok=True)
  os.makedirs('output/react_app/src/store/slices', exist_ok=True)
  os.makedirs('output/react_app/src/api', exist_ok=True)
  ```

### File Creation
- All files must be created using Code Interpreter's file writing capabilities
- Verify directory structure exists before writing files
- Use absolute paths when needed for file operations

### Build and Verification
- After creating all files, verify the build works:
  ```python
  import subprocess
  import os
  
  # Change to directory
  os.chdir('output/react_app')
  
  # Install dependencies
  subprocess.run(['npm', 'install'], check=True)
  
  # Build the app
  subprocess.run(['npm', 'run', 'build'], check=True)
  ```
- Only mark task complete when build succeeds without errors
- If build fails, fix errors before completing

## Critical Implementation Details

1. Bootstrap CSS must be imported before custom CSS
2. All form inputs must be controlled components
3. Redux state must be the single source of truth
4. All actions must be dispatched, never mutate state directly
5. Components must handle empty states gracefully
6. Number formatting (toFixed(2)) for currency display
7. Conditional styling for profit/loss colors
8. Responsive breakpoint at 768px
9. All buttons must have hover effects
10. All inputs must have focus states

