using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class ShaderPropertyExposer : MonoBehaviour
{

    // public float control;
    private TextMeshProUGUI tmPro;
    private Material tmProMat;
    public Color newColor = new Color(0f, 0f, 0f, 0.5f);

    // Start is called before the first frame update
    void Start()
    {
        tmPro = GetComponent<TextMeshProUGUI>();
        tmProMat = tmPro.fontMaterial;
    }

    // Update is called once per frame
    void Update()
    {
        tmProMat.SetColor("_UnderlayColor", newColor);
    }
}
