wrk.method = "POST"
wrk.headers["Accept"] = "application/json"
wrk.headers["Content-Type"] = "application/json"
local inputs = {
    "In what year was the winner of the 44th edition of the Miss World competition born?",
    "Author David Chanoff has collaborated with a U.S. Navy admiral who served as the ambassador to the United Kingdom under which President?",
    "Create a table for top noise cancelling headphones that are not expensive",
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