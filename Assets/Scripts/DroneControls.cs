using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class DroneControls : MonoBehaviour
{
    public Rigidbody rb;
    //inputs we will read from the radio
    private float yawInput = 0;
    private float rollInput = 0;
    private float pitchInput = 0;
    private float throttleInput = 0;

    private Transform trans;

    //properties of the player's settings
    //To-Do: read these from a save file
    [SerializeField] private bool midThrottle = true;
    [SerializeField] private float superRate = 70.0f;
    [SerializeField] private float rcRate = 90.0f;
    [SerializeField] private float rcExpo = 0.0f;
    [SerializeField] private bool superExpoActive = true;
    [SerializeField] private float thrust = 25.0f;
    //[SerializeField] private int rate = 300;

    void Start()
    {
        //get this asset's RigidBody component
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per physics frame
    void FixedUpdate() {
        Joystick joystick = Joystick.current;
        calculateThrust();
        calculateRotation();
    }

    public void calculateThrust()
    {
        rb.AddRelativeForce(Vector3.up * throttleInput * thrust,ForceMode.Force);
    }

    public void calculateRotation()
    {
        //let's get RC values similar to what we'd see in Betaflight (aka 1000 - 2000)
        float pitchRCValue = ((-pitchInput*0.5f)+1.5f)*1000f;
        float yawRCValue = ((yawInput*0.5f)+1.5f)*1000f;
        float rollRCValue = ((-rollInput*0.5f)+1.5f)*1000f;

        //let's run that through the betaflight rate system to get our degrees per second setpoint for each axis
        float pitchDPS = stickInputToDPS(pitchRCValue);
        float yawDPS = stickInputToDPS(yawRCValue);
        float rollDPS = stickInputToDPS(rollRCValue);
        //Debug.Log("pitch: "+pitchDPS.ToString());
        //Debug.Log("yaw: "+yawDPS.ToString());
        //Debug.Log("roll: "+rollRCValue.ToString());
        rb.angularVelocity = transform.TransformDirection(new Vector3(pitchDPS, yawDPS, rollDPS));
        //transform.rotation = transform.rotation * Quaternion.Euler(new Vector3(pitchInput, yawInput , rollInput));
        //-1,1 * 0.5
        //1,3
    }

    public float stickInputToDPS(float rcData)
    {
        float inputValue = rcCommand(rcData, rcRate, rcExpo);
        float angleRate = 0.0f;
        if (superExpoActive)
        {
            float rcFactor = Mathf.Abs(inputValue) / (500f * rcRate / 100f);
            rcFactor = 1f / (1f - rcFactor * superRate / 100f);
            angleRate = rcFactor * 27f * inputValue / 16f;
        }
        else
        {
            angleRate = (superRate + 27f) * inputValue / 16f;
        }
        //angleRate = constrain(angleRate, -8190, 8190); // Rate limit protection
        return angleRate/230f;
    }

    public float rcCommand(float rcData, float rcRate, float rcExpo)
    {
        float midRc = 1500f;
        float tmp = Mathf.Abs(rcData - midRc) / 100f;
        float result = ((2500f + rcExpo * (tmp * tmp - 25f)) * tmp * rcRate / 2500f);
        if (rcData < midRc)
        {
            result = -result;
        }
        return result;
    }

    public void OnThrottle(InputValue value)
    {


        if(midThrottle==true){
            throttleInput = (value.Get<float>());
            if(throttleInput<0.0f){
                throttleInput = 0.0f;
            }
        }else{
            throttleInput = (1.0f+value.Get<float>())/2.0f;
        }
    }

    public void OnYaw(InputValue value)
    {
        yawInput = value.Get<float>();
    }

    public void OnPitch(InputValue value)
    {
        pitchInput = value.Get<float>();
    }

    public void OnRoll(InputValue value)
    {
        rollInput = value.Get<float>();
    }
}
