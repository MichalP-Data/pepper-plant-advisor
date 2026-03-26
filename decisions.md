# Decisions: Pepper Assistant LLM Integration

Date: 2026-03-26

This document records the architectural and product decisions made for the "Hot Pepper Grow Assistant" MVP.

1. App structure
   - Decision: Create a new Django app named `pepper_assistant`.
   - Rationale: Clear separation of concerns and better presentation in portfolio. Keeps the original `chat` app untouched.

2. Conversations
   - Decision: Single default conversation for MVP (auto-created on first visit).
   - Rationale: Simplifies UI and demonstration; supports requirements (not multi-user).

3. Message roles
   - Decision: Use `user` and `assistant` roles.
   - Rationale: Matches typical LLM chat API patterns and is sufficient for MVP.

4. LLM integration
   - Decision: Implement a mock `generate_pepper_response(...)` now. Provide an easy switch to a real API later via environment variables (`LLM_PROVIDER`, `LLM_API_KEY`).
   - Rationale: Quick demo and offline development. Keeps code modular for replacement.

5. Sync vs Async
   - Decision: Use synchronous request-response flow in a standard Django view.
   - Rationale: Simpler to implement and aligns with tech constraint to avoid Celery/Redis.

6. UI/UX
   - Decision: Display last 50 messages in chronological order. Simple, readable UI in English.
   - Rationale: Limits data sent to templates and keeps UI performant.

7. Validation
   - Decision: Enforce `max_length=2000` on message content and require non-empty input.
   - Rationale: Prevents huge messages and keeps DB safe.

8. Security
   - Decision: Do not store secrets in repository. Use environment variables for `SECRET_KEY` and LLM credentials.
   - Rationale: Follows best practices and GitHub instructions.

9. Tests & CI
   - Decision: Add simple model and view tests and a GitHub Actions workflow to run `python manage.py test`.
   - Rationale: Demonstrates professional practices in portfolio.

10. Admin
    - Decision: Register `Conversation` and `Message` in Django admin with helpful list displays and filters.
    - Rationale: Makes it easy to inspect stored conversations and messages.

11. Deployment
   - Decision: Support deployment to Vercel for quick portfolio hosting. Add CI workflow to run tests and optionally deploy via Vercel CLI when `VERCEL_TOKEN` secret is set. Provide Dockerfile and `vercel.json` to help Vercel detect the project if needed.
   - Rationale: Vercel can host small projects quickly; using CI to gate deploys ensures tests pass before deployment. Note: Django may require Docker or a proper build command on Vercel; consider Render or Railway for simpler Django hosting if issues arise.

12. Prompt engineering & safety
   - Decision: Keep prompt logic in `services/llm_service.py`. Start with mock rules and add a `system` instruction and safety disclaimer when switching to a real LLM. The assistant will avoid giving medical/treatment dosages and will include a short disclaimer for medical/toxicological questions.
   - Rationale: Centralized prompt logic makes it easy to iterate, A/B test, or replace with provider-specific code.

      13. UI library
         - Decision: Use Tailwind CSS + daisyUI (via CDN) for improved, modern UI in the MVP.
         - Rationale: Small dependency footprint, improved visuals, quick to integrate with templates via CDN.

      14. LLM response length
         - Decision: Cap responses to ~300 tokens (simulated in mock) and provide an option for the user to ask follow-ups for more detail.
         - Rationale: Short, digestible answers are better for UI and user experience.

                  15. Conversation context limit
                     - Decision: Send the last N=10 messages as context to the LLM (simulated in mock). This keeps the prompt focused and bounds token usage.
                     - Rationale: Provides useful context for follow-ups without sending the entire history.

                  16. CI Vercel action
                     - Decision: Use `amondnet/vercel-action@v20` in GitHub Actions to perform Vercel deploys when `VERCEL_TOKEN` is set.
                     - Rationale: Simpler and more robust than installing the Vercel CLI during workflow.

Notes:
- The mock LLM service is implemented in `pepper_assistant/services/llm_service.py` and returns domain-relevant answers based on simple keyword matching.
- Replacing the mock with a real LLM provider should require only changes in the `services` module to call the provider's API.

