wrk.method = "POST"
wrk.headers["Accept"] = "application/json"
wrk.headers["Content-Type"] = "application/json"
local inputs = {
    "What is the capital of France?",
    "Who wrote 'To Kill a Mockingbird'?",
    "What is the speed of light?",
}

math.randomseed(os.time())
local random_input = inputs[math.random(#inputs)]

wrk.body = '{"inputs": "' .. random_input .. '"}'

function response(status, headers, body)
    if status ~= 200 then
        print('Status: ' .. status)
        print('Body: ' .. body)
    end
end