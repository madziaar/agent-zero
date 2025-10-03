# Security Code Review Prompt Template

**Qwen Model Optimization**: 14B (Security analysis with comprehensive vulnerability assessment)

```
Conduct a comprehensive security review of this application with focus on identifying and mitigating potential vulnerabilities:

**Security Assessment Framework:**

**Authentication & Authorization:**
- Password storage mechanisms and strength requirements
- Session management and token security implementation
- Access control mechanisms and privilege escalation prevention
- Multi-factor authentication implementation review
- Account lockout and brute force protection mechanisms

**Input Validation & Sanitization:**
- SQL injection prevention through parameterized queries and ORM usage
- XSS (Cross-Site Scripting) vulnerability assessment in all user input handling
- CSRF (Cross-Site Request Forgery) protection mechanisms
- File upload validation and malicious file prevention
- Command injection prevention in system calls and external processes

**Cryptographic Implementation:**
- Encryption algorithm strength and proper key management
- TLS/SSL configuration and certificate validation
- Hash function security for password storage and data integrity
- Secure random number generation for tokens and keys
- Cryptographic key rotation and storage security

**Data Protection & Privacy:**
- Sensitive data identification and classification
- Data encryption at rest and in transit
- GDPR, CCPA, and other privacy regulation compliance
- Data retention and secure deletion procedures
- User consent management and privacy policy implementation

**Network & Infrastructure Security:**
- Network architecture security assessment
- Firewall configuration and network segmentation
- DDoS protection and rate limiting implementation
- Secure header configuration and security headers
- API security and endpoint protection mechanisms

**Error Handling & Information Disclosure:**
- Error message security and information leakage prevention
- Stack trace exposure in production environments
- Debug information removal from production builds
- Secure logging practices and log injection prevention
- User-friendly error messages without technical details

**Security Testing Requirements:**
- Static Application Security Testing (SAST) integration
- Dynamic Application Security Testing (DAST) implementation
- Dependency vulnerability scanning and management
- Penetration testing scope and methodology
- Security regression testing in CI/CD pipeline

**Compliance & Standards:**
- OWASP Top 10 coverage assessment and mitigation strategies
- Industry-specific security standards compliance
- Security audit trail and logging requirements
- Incident response and breach notification procedures
- Security awareness training and documentation

**Deliverables:**
1. Executive security summary with overall risk assessment
2. Detailed vulnerability findings with CVSS scores and severity levels
3. Prioritized remediation roadmap with implementation guidance
4. Security testing strategy and automated testing recommendations
5. Compliance validation report with gap analysis and remediation steps
6. Security monitoring and alerting configuration guidelines
7. Incident response procedures and escalation protocols

**Success Criteria:**
- Zero critical or high-severity vulnerabilities in final assessment
- Complete OWASP Top 10 coverage with mitigation strategies
- Compliance with relevant security standards and regulations
- Comprehensive security testing integration in development lifecycle
- Documented security procedures for operations team
- Security awareness and training program implementation

Focus on creating a production-ready application with enterprise-grade security that can withstand sophisticated attack vectors while maintaining usability and performance.
```
