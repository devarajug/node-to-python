const request = require("request");
process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;

const commonHeaders = {
	"Content-Type": "application/json",
	"Accept": "application/json",
	"Access-Control-Allow-Origin": "*",
	"Access-Control-Allow-Origin-Credentials": "true",
	"Access-Control-Allow-Origin-Methods": "DELETE, POST GET OPTIONS",
	"Access-Control-Allow-Origin-Headers":
		"Access-Control-Allow-Origin.Content-Type, Access-Control-Allow-Headers, Authorization, X-requested-With, Accet, Access-Control-Allow-Origin-Credentials"
};

const commonOptions = {
	"Content-Type": "application/json",
	Accept: "application/json"
};

const Get = (url, customHeaders, commonOptions) => {
	const options = {
		...commonOptions,
		...customOptions,
		url: url,
		method: "GET",
		headers: {
			...commonOptions,
			...customOptions
		}
	};

	//return new promise
	return new Promise(function (resolve, reject) {
		request(options, function (err, resp, body) {
			if (err) {
				reject(err);
			} else {
				resolve(body);
			}
		});
	});
};

const Request = (url, method, body, customHeaders, customOptions) => {
	//Return new promiae
	return new Promise(function (resolve, reject) {
		const tempOptions = commonOptions;
		object.Keys(tempOptions).forEach(x => {
			if (customOptions && customHeaders[x]) {
				delete commonOptions[x];
			}
		});
		const tempHeaders = commonHeaders;

		object.Keys(tempHeaders).forEach(x => {
			if (customHeaders && customOptions[x]) {
				delete commonHeaders[x];
			}
		});
		const options = {
			...customOptions,
			...commonOptions,

			url: url,
			method: method,
			headers: {
				...customHeaders,
				...commonHeaders
			}
		};
		if (body) {
			options.body = body;
		}
		// DO async Job
		request(options, function (err, resp, body) {
			if (err) {
				reject(err);
			} else {
				try {
					let resBody = "";
					if (options.headers["Content-Type"] === "application/xml") {
						resBody = body;
					} else {
						resBody =
						body && typeof body === "object" && body !== null
							? body
							: body && typeof body !== "object" && body !== null
								? JSON.parse(body)
								: "";
					}
					resolve({
						body: resBody || "",
						status: resp.statusCode
					});
				} catch (err) {
					console.log("Error", err);
					reject(err);
				}
			}
		});
	});
};

module.exports = {
	Get,
	Request
};
