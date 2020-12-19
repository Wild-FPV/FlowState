using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class DroneConfigurationSettings : MonoBehaviour
{

    public GameObject RollRate;
    public GameObject RollSuper;
    public GameObject RollExpo;
    public GameObject PitchRate;
    public GameObject PitchSuper;
    public GameObject PitchExpo;
    public GameObject YawRate;
    public GameObject YawSuper;
    public GameObject YawExpo;

    void Start() {
        if (PlayerPrefs.HasKey("RollRate")) {
            RollRate.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("RollRate");
        }
        if (PlayerPrefs.HasKey("RollSuper")) {
            RollSuper.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("RollSuper");
        }
        if (PlayerPrefs.HasKey("RollExpo")) {
            RollExpo.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("RollExpo");
        }
        if (PlayerPrefs.HasKey("PitchRate")) {
            PitchRate.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("PitchRate");
        }
        if (PlayerPrefs.HasKey("PitchSuper")) {
            PitchSuper.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("PitchSuper");
        }
        if (PlayerPrefs.HasKey("PitchExpo")) {
            PitchExpo.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("PitchExpo");
        }
        if (PlayerPrefs.HasKey("YawRate")) {
            YawRate.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("YawRate");
        }
        if (PlayerPrefs.HasKey("YawSuper")) {
            YawSuper.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("YawSuper");
        }
        if (PlayerPrefs.HasKey("YawExpo")) {
            YawExpo.GetComponent<TMP_InputField>().text = PlayerPrefs.GetString("YawExpo");
        }
    }

    public void SaveDroneConfiguration() {
        PlayerPrefs.SetString("RollRate", RollRate.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("RollSuper", RollSuper.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("RollExpo", RollExpo.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("PitchRate", PitchRate.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("PitchSuper", PitchSuper.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("PitchExpo", PitchExpo.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("YawRate", YawRate.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("YawSuper", YawSuper.GetComponent<TMP_InputField>().text);
        PlayerPrefs.SetString("YawExpo", YawExpo.GetComponent<TMP_InputField>().text);
        PlayerPrefs.Save();
    }
}
