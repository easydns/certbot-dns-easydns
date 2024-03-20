Change notes for certbot-dns-easydns
====================================

### v0.1.0: Initial version
	- Largely based on plugins for ISPConfig, DNSMadeEasy, DNSimple
	- Uses Lexicon which support EasyDNS as a provider.
	- Requires that EasyDNS is the DNS provider for the domain to be
      used.  Customers may register to receive access to the REST API
      which is required for this Authenticator to work.

### v0.1.1: Documentation Improvements
	- Updated example commandlines to match reality.
	- Some reformatting of README.rst

### v0.1.2: More Documentation Improvements
    - Corrected inline command-line argument example.
	- Enhanced documentation around creation and specification of the credentials file.

### v0.1.3: Correct typo in Docker example
    - There was a typo in the Docker compose example; it has been corrected

### v0.1.4: Correct bug in `_handle_http_error`
	- When the API receives a request for a domain it doesn't
      recognize, it returns server code 400 rather than 404, so it was
      necessary to look for both in the error handler.  This should mean
      that subdomains can now get certs.
