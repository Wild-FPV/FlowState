using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;
using TMPro;

public class RadioBinding : MonoBehaviour
{

    private Joystick currentJoystick = Joystick.current;
    public GameObject ChannelOneText;
    public GameObject ChannelOneSlider;

    void FixedUpdate() {

        ChannelOneText.GetComponent<TMP_Text>().text = currentJoystick.stick.y.ReadValue().ToString();
        ChannelOneSlider.GetComponent<Slider>().value = currentJoystick.stick.y.ReadValue();

        Debug.Log( Joystick.current["/rx"] );
    }
}


