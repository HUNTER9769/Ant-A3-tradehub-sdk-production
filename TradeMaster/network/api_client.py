from utility.library import *


class RequestHandler:
    def __init__(self, session_token: str, proxy_url: str = None, static_ip: str = None):
        """
        Initializes the request handler with a session token.

        Args:
            session_token (str): Authorization token for API calls.
        """
        self.headers = {
            "Authorization": session_token
        }

        # proxy settings
        self.proxy_url = proxy_url
        self.static_ip = static_ip

        self.enable_logs = True

    def _log(self, stage, data=None):
        if not self.enable_logs:
            return
        print(f"[RH:{stage}]", data if data else "")

    def request(self, url: str, method: str, data=None, params=None) -> dict:
        """
        Sends an API request and handles the response.

        Args:
            url (str): Endpoint URL.
            method (str): API method - GET, POST, PUT, DELETE.
            data (dict or str, optional): Request payload.
            params (dict, optional): Query parameters.

        Returns:
            dict: Parsed JSON response or error structure.
        """
        try:
            self._log("ENTER", {"method": method, "url": url})

            method = method.upper()

            kwargs = {
                "headers": self.headers,
            }

            if isinstance(params, dict):
                kwargs["params"] = params

            if data is not None:
                kwargs["json"] = data

            self._log("PROXY_REQUEST", {
                "proxy": self.proxy_url,
                "ip": self.static_ip
            })
            # =========================
            # PROXY FLOW
            # =========================
            if self.proxy_url:

                proxy_payload = {
                    "method": method,
                    "url": url,
                    "source_ip": self.static_ip,
                    "headers": self.headers,
                    "params": params if isinstance(params, dict) else {},
                    "json": data,
                    "timeout": 20,
                    "allow_redirects": True,
                    "verify_ssl": True
                }

                response = requests.post(
                    self.proxy_url,
                    json=proxy_payload,
                    timeout=25
                )

                self._log("PROXY_RESPONSE_RAW", {
                    "status": response.status_code,
                    "text": response.text[:300]
                })

                if response.status_code != 200:
                    return {
                        'stat': 'Not_ok',
                        'emsg': response.text,
                        'encKey': None
                    }

                result = response.json()

                self._log("PROXY_RESPONSE", result)

                return result.get("json") or {
                    'stat': 'Not_ok',
                    'emsg': result.get("text"),
                    'encKey': None
                }

            # =========================
            # DIRECT FLOW
            # =========================
            self._log("DIRECT_REQUEST")

            if method == "POST":
                response = requests.post(url, timeout=20, **kwargs)
            elif method == "GET":
                response = requests.get(url, timeout=20, **kwargs)
            elif method == "PUT":
                response = requests.put(url, timeout=20, **kwargs)
            elif method == "DELETE":
                response = requests.delete(url, timeout=20, **kwargs)
            else:
                raise ValueError(f"Unsupported request type: {method}")

            self._log("DIRECT_RESPONSE", {
                "status": response.status_code,
                "text": response.text[:300]
            })

            return self._handle_response(response)

        # =========================
        # ERRORS
        # =========================
        except requests.ConnectionError as e:
            self._log("CONNECTION_ERROR", str(e))
            return {'stat': 'Not_ok', 'emsg': str(e), 'encKey': None}

        except requests.Timeout as e:
            self._log("TIMEOUT", str(e))
            return {'stat': 'Not_ok', 'emsg': str(e), 'encKey': None}

        except ValueError as e:
            self._log("VALUE_ERROR", str(e))
            return {'stat': 'Not_ok', 'emsg': str(e), 'encKey': None}

        except Exception as e:
            self._log("EXCEPTION", str(e))
            return {'stat': 'Not_ok', 'emsg': str(e), 'encKey': None}

    def _handle_response(self, response: requests.Response) -> dict:
        """
        Parses the response object and returns a structured result.

        Args:
            response (requests.Response): Response from the request.

        Returns:
            dict: Parsed response or error structure.
        """
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'stat': 'Not_ok',
                'emsg': f"{response.status_code} - {response.reason}",
                'encKey': None
            }
