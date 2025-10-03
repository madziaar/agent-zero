# React Component Generation Prompt

**Qwen Model Optimization**: 14B (Balanced complexity and quality)

```
Generate a modern React component for a dashboard with data visualization:

**Component Requirements:**
- Display key metrics in card format (revenue, users, orders, conversion rate)
- Interactive charts using Chart.js or Recharts
- Responsive grid layout with Material-UI or Chakra UI
- Real-time data updates with WebSocket integration
- Loading states and error handling
- Dark/light theme support

**Technical Specifications:**
- React 18+ with hooks (useState, useEffect, useCallback)
- TypeScript for type safety
- Custom hooks for data fetching and WebSocket management
- Error boundaries for graceful error handling
- Accessibility features (ARIA labels, keyboard navigation)
- Performance optimization (React.memo, useMemo)

**Code Quality Standards:**
- Comprehensive unit tests with Jest and React Testing Library
- Storybook documentation for component variations
- ESLint and Prettier configuration
- Performance monitoring with React DevTools Profiler
- Responsive design breakpoints
- Cross-browser compatibility

**Integration Requirements:**
- Redux Toolkit or Zustand for state management
- React Query or SWR for server state management
- React Router for navigation integration
- i18next for internationalization support
- Environment-based configuration

**Deliverables:**
1. Main Dashboard component with all features
2. Individual MetricCard component
3. Custom hooks for data management
4. Chart configuration utilities
5. Complete test suite
6. Storybook stories
7. Documentation with usage examples

**Success Criteria:**
- Component renders correctly across all screen sizes
- All interactive features work as expected
- Performance metrics meet targets (<100ms render time)
- Accessibility score > 95 in Lighthouse
- Test coverage > 90%
- No ESLint errors or warnings

Focus on creating a production-ready, maintainable component that follows React best practices and provides an excellent user experience.
```
