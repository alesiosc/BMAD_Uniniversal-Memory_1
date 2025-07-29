# Testing Strategy

### Testing Pyramid
Our strategy will focus on a large base of fast and isolated unit tests, a smaller layer of integration tests to verify component interactions, and a select few end-to-end tests for critical user workflows.

```text
      /     \
     /  E2E  \
    /---------\
   /Integration\
  /-------------\
 /  Unit Tests   \
/-----------------\