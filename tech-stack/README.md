# Tech Stack Detector

The Tech Stack Detector is a powerful enhancement that enables Agent OS to automatically detect and adapt to the specific technology stack of your project. This is particularly useful when working on multiple projects with different technology stacks, as it allows the agent to generate code and follow standards that are appropriate for each project.

## Key Features

- **Automatic Detection:** The detector automatically scans your project to identify the programming languages, frameworks, databases, and tools you are using.
- **Multi-Stack Support:** The system can handle projects with multiple technology stacks, such as microservices architectures.
- **Dynamic Standards:** The detector can generate and adjust Agent OS standards based on the detected tech stack, ensuring that the agent follows the correct conventions for your project.
- **Stack Validation:** The system can validate your existing Agent OS standards against the detected tech stack to identify any inconsistencies.

## How It Works

The Tech Stack Detector works by analyzing the files in your project, such as `package.json`, `requirements.txt`, and `Gemfile`, to identify the technologies you are using. It then uses this information to create a detailed profile of your project's tech stack.

Once the tech stack has been detected, the system can use this information to:

- **Generate a `tech-stack.md` file** that documents the detected technologies.
- **Create language- and framework-specific standards** that the agent will follow when generating code.
- **Validate your existing standards** to ensure they are consistent with the detected tech stack.

## Usage

The Tech Stack Detector is enabled by default in the enhanced version of Agent OS. You can configure its behavior in the `config/enhanced-config.yml` file.

To use the tech stack detector, you can run the `stack-detector.py` script:

```bash
# Detect the tech stack of your project
python3 .agent-os/tech-stack/stack-detector.py --detect

# Generate standards based on the detected tech stack
python3 .agent-os/tech-stack/stack-detector.py --generate-standards --output-dir .agent-os/standards
```

## Benefits

- **Improved Accuracy:** By understanding the specific tech stack of your project, the agent can generate more accurate and appropriate code.
- **Increased Consistency:** The dynamic standards feature ensures that the agent always follows the correct conventions for your project, improving code consistency.
- **Reduced Manual Configuration:** The automatic detection feature reduces the need for you to manually configure the agent for each project, saving you time and effort.
- **Better Support for Diverse Projects:** The multi-stack support feature makes it easier to use Agent OS on a wide range of projects, including those with complex microservices architectures.


