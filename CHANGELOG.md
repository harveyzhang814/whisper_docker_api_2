# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Initial project structure planning
- Added detailed README documentation
- Planned support for multi-model, multi-format, and streaming Whisper API
- 新增音频分片和转 base64 工具函数（split_audio, audio_to_base64），并在测试脚本中实现复用，提升了流式接口测试的可维护性和复用性。
- Improved code comments and docstrings throughout the codebase for better readability and maintainability.

## [0.1.0] - 2024-06-1
### Added
- Added Docker deployment support: Dockerfile and docker-compose.yml for easy containerization
- Added .dockerignore to optimize Docker image build
- Updated documentation for API usage and deployment 

## [0.1.0] - 2024-06-11
### Added
- Project initialized
- Added README.md with project overview, features, API design, and usage instructions 

## [Unreleased] - 2024-06-11

### Changed
- Refactored `API_GUIDE.md` to clarify best usage practices, including:
  - Improved instructions for preparing and sending audio data.
  - Enhanced error handling documentation.
  - Added more detailed examples for both HTTP and WebSocket usage.
  - Updated FAQ and notes for common user questions.
