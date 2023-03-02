certbot-dns-easydns
=====================

EasyDNS_ DNS Authenticator plugin for Certbot_

This plugin automates the process of completing a ``dns-01`` challenge by
creating, and subsequently removing, TXT records using the EasyDNS REST API.

Configuration of EasyDNS
------------------------

As an EasyDNS_ user with at least one domain being served by EasyDNS,
log into the control panel and navigate under "User" to "Security" and
then to the bottom, to the REST API section.  You may need to complete
the registration form in order to receive credentials, but they should
be issued automatically once the form is submitted.

The user token is like a username or public key, but should probably
still be kept confidential.  The API key is issued by clicking
"Regenerate" and is only shown for a short time in the browser and
then never again; be ready to copy it and stuff it into some sort
of protected datastore.  Both must be used together to authenticate
with the API.  See below about how to create a file for the credentials.

It is possible to direct the endpoint, but the default is for the
plugin to use the production API endpoint.  The sandbox endpoint does
not create actual changes to DNS, and so cannot be used to issue
certificates.

.. _EasyDNS: https://www.easydns.com/
.. _certbot: https://certbot.eff.org/

Installation
------------

::

    pip install certbot-dns-easydns


Named Arguments
---------------

To start using DNS authentication for EasyDNS, pass the following arguments on
certbot's command line:

============================================================= ==============================================
``--authenticator certbot-dns-easydns:dns-easydns``           select the authenticator plugin (Required)

``--certbot-dns-easydns:dns-easydns-credentials``             EasyDNS Remote User credentials
                                                              INI file. (Required)

``--certbot-dns-easydns:dns-easydns-propagation-seconds``     | waiting time for DNS to propagate before asking
                                                              | the ACME server to verify the DNS record.
                                                              | (Default: 120, Recommended: >= 600)
============================================================= ==============================================

(Note that the verbose and seemingly redundant ``certbot-dns-easydns:`` prefix
is currently imposed by certbot for external plugins.)


Credentials
-----------

An example ``credentials.ini`` file:

.. code-block:: ini

   certbot_dns_easydns:dns_easydns_usertoken = myremoteuser
   certbot_dns_easydns:dns_easydns_userkey = verysecureremoteuserpassword


The path to this file can be provided interactively or using the
``--certbot-dns-easydns:dns-easydns-credentials`` command-line argument. Certbot
records the path to this file for use during renewal, but does not store the
file's contents.

**CAUTION:** You should protect these API credentials as you would the
password to your EasyDNS account. Users who can read this file can use these
credentials to issue arbitrary API calls on your behalf. Users who can cause
Certbot to run using these credentials can complete a ``dns-01`` challenge to
acquire new certificates or revoke existing certificates for associated
domains, even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).


Examples
--------

To acquire a single certificate for both ``example.com`` and
``*.example.com``, waiting 900 seconds for DNS propagation:

.. code-block:: bash

   certbot certonly \
     --authenticator certbot-dns-easydns:dns-easydns \
     --certbot-dns-easydns:dns-easydns-credentials /etc/letsencrypt/.secrets/domain.tld.ini \
     --certbot-dns-easydns:dns-easydns-propagation-seconds 900 \
     --server https://acme-v02.api.letsencrypt.org/directory \
     --agree-tos \
     --rsa-key-size 4096 \
     -d 'example.com' \
     -d '*.example.com'


Docker
------

In order to create a docker container with a certbot-dns-easydns installation,
create an empty directory with the following ``Dockerfile``:

.. code-block:: docker

    FROM certbot/certbotb
    RUN pip install certbot-dns-easydns

Proceed to build the image::

    docker build -t certbot/dns-easydns .

Once that's finished, the application can be run as follows::

    docker run --rm \
       -v /var/lib/letsencrypt:/var/lib/letsencrypt \
       -v /etc/letsencrypt:/etc/letsencrypt \
       --cap-drop=all \
       certbot/dns-easydns certonly \
       --authenticator certbot-dns-easydns:dns-easydns \
       --certbot-dns-easydns:dns-easydns-propagation-seconds 900 \
       --certbot-dns-easydns:dns-easydns-credentials \
           /etc/letsencrypt/.secrets/domain.tld.ini \
       --no-self-upgrade \
       --keep-until-expiring --non-interactive --expand \
       --server https://acme-v02.api.letsencrypt.org/directory \
       -d example.com -d '*.example.com'

It is suggested to secure the folder as follows::
chown root:root /etc/letsencrypt/.secrets
chmod 600 /etc/letsencrypt/.secrets