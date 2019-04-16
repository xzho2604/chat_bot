
#store samples of a context
name: "projects/weather-f22a9/agent/sessions/first/contexts/lights"
lifespan_count: 5
parameters {
  fields {
    key: "device"
    value {
      string_value: "light bulb"
    }
  }
  fields {
    key: "device.original"
    value {
      string_value: "light"
    }
  }
  fields {
    key: "intent_action"
    value {
      string_value: "IOT.turn_on"
    }
  }
}
