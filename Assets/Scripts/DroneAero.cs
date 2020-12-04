using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DroneAero : MonoBehaviour
{
    private Rigidbody rb;

    [SerializeField] float dragMultiplier = 50f;
    //[SerializeField] float liftMultiplier = 50f;
    [SerializeField] float surfaceArea = 1f;
    [SerializeField] Vector3 parasiticDrag = new Vector3(0.0f,0.0f,0.0f);
    [SerializeField] Vector3 debug;
    void Start()
    {
        //get this asset's RigidBody component
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        //let's calculate the induced and parasitic drag forces
        Vector3 parasiticDrag = calculateParasiticDrag();
        Vector3 inducedDrag = calculateInducedDrag();
        applyAero(parasiticDrag, inducedDrag);
    }

    void applyAero(Vector3 pDrag, Vector3 iDrag)
    {
        //rb.AddRelativeForce(pDrag,ForceMode.Force);
        //float mass = 0.5f;
        //rb.AddForce(0, -9.8f*10f*mass, 0,ForceMode.Force);
        rb.AddForce(pDrag,ForceMode.Force);
        rb.AddForce(iDrag,ForceMode.Force);
        //switchback = 0.17x0.17 meters

    }

    //This method estemates the parasitic drag force on the drone
    Vector3 calculateParasiticDrag()
    {
        //Vector3 parasiticDrag = new Vector3(0.0f,0.0f,0.0f);

        float pDrag = 0.15f; //the magic parasitic drag number (needs to be measured)
        pDrag += ((dragMultiplier-70f)/1000f); //allow's users' (0 - 100) value to be +/- 0.05 of our magic number

        //TO_DO: this should be based on actual serfice area and validated
        float surfaceAreaMultiplier = Mathf.Pow(surfaceArea, 0.75f); //let's allow larger drones to generate both more drag and lift
        pDrag = surfaceAreaMultiplier*(pDrag);

        //let's get the angle of attack by finding angle between the quad's velocity and it's orientation
        Vector3 velocity = rb.velocity;
        Vector3 orientation = rb.transform.rotation.eulerAngles;

        parasiticDrag = new Vector3(-velocity.x*pDrag,-velocity.y*pDrag,-velocity.z*pDrag);

        return parasiticDrag;
    }

    Vector3 calculateInducedDrag()
    {
        Vector3 inducedDrag = new Vector3(0.0f,0.0f,0.0f);

        float iDrag = 0.25f; //the magic induced drag number (needs to be measured)
        iDrag += ((dragMultiplier-70f)/1000f); //allow's users' (0 - 100) value to be +/- 0.05 of our magic number

        //TO_DO: this should be based on actual serfice area and validated
        float surfaceAreaMultiplier = Mathf.Pow(surfaceArea, 0.75f); //let's allow larger drones to generate both more drag and lift
        iDrag = surfaceAreaMultiplier*(iDrag);

        //let's get the angle of attack by finding angle between the quad's velocity and it's orientation
        Vector3 velocity = rb.velocity;
        Vector3 quadUpVector = rb.transform.up;



        float angleOfAttack = Vector3.Angle(velocity,quadUpVector);
        angleOfAttack = ((angleOfAttack-90f))/90f; //instead of 0 - 180, we want a range of -1, to 1
        inducedDrag = rb.transform.up*angleOfAttack*velocity.magnitude*iDrag;

        debug = inducedDrag;

        return inducedDrag;
    }
}
