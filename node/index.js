const route = require("./route");
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0;
module.exports.handler = async (event, context, callback) => {
	try {
		const routes = await route(event.path);
		const requestHandler = await routes[event.httpMethod];
		const response = await requestHandler(event);

		callback(null. {
			statusCode: 200,
			body: JSON.stringify(response),
			headers: {"Access-Control-Allow-Origin": process.env.CORS_DOMAIN}
		});

	} catch (err) {
		comsole..error(err);
		callback(null, {
			statusCode: 400,
			body: err,
			headers: {"Access-Control-Allow-Origin": process.env.CORS_DOMAIN}
		});
	}
};
