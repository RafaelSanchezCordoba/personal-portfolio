# Diagram sources

Run `python3 render_diagrams.py` to regenerate the three SVGs in `../assets/`. Uses the Python standard library only.

Conventions: cloud deployment/service view, UML sequence lifelines for the CI/CD flow, and explicit trust boundaries for the security view. Same palette, typography and arrow markers as the Maitecrafts diagrams.

No brand icons here, unlike Maitecrafts: the AWS services in this project have no consistent icon set in the local `icons/` collection, so services are drawn as labelled nodes instead of mixing sourced glyphs with improvised ones.

Every value shown (regions, resource names, policy conditions, commands) is copied from `infrastructure/*.tf` and `.github/workflows/deploy-aws.yml` on the `aws-deployment` branch. The AWS account ID is not shown anywhere.
