using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;
using UnityEngine.Networking;

public class LoadMap : MonoBehaviour
{
    [SerializeField] string mapName;


    void Start () {
        var myLoadedAssetBundle = AssetBundle.LoadFromFile(Path.Combine(Application.streamingAssetsPath, "standardmapelements"));
        if (myLoadedAssetBundle == null)
        {
            Debug.Log("Failed to load AssetBundle!");
            return;
        }

        var mapFile = ReadMap(mapName);
        FSMap map = JsonUtility.FromJson<FSMap>(mapFile);

        List<MapAsset> mapAssets = map.assets;
        foreach (var asset in mapAssets) {

            string assetName = asset.n;
            Debug.Log("added new asset: "+assetName);
            List<float> assetPosition = asset.p;
            List<float> assetOrientation = asset.o;
            List<float> assetScale = asset.s;
            var newAsset = myLoadedAssetBundle.LoadAsset<GameObject>(assetName);

            if(newAsset!=null){
                GameObject assetInstance = (GameObject)Instantiate(newAsset);
                Debug.Log("added "+assetName);
                assetInstance.transform.position = new Vector3(assetPosition[0]*0.1F, assetPosition[2]*0.1F, assetPosition[1]*0.1F);
                assetInstance.transform.eulerAngles  = new Vector3(assetOrientation[0], assetOrientation[2], assetOrientation[1]);
                assetInstance.transform.localScale = new Vector3(assetScale[0], assetScale[2], assetScale[1]);
                if(assetName=="asset launch pad"){
                    GameObject drone = GameObject.Find("Test Drone Switchback");
                    drone.transform.position = new Vector3(assetPosition[0]*0.1F, (assetPosition[2]*0.1F)+0.5F, assetPosition[1]*0.1F);
                    drone.transform.eulerAngles  = new Vector3(assetOrientation[0], assetOrientation[2], assetOrientation[1]);
                }
            }else{
                Debug.Log("unable to add "+assetName);
            }
        }

        myLoadedAssetBundle.Unload(false);
    }

    static string ReadMap(string mapName)
    {
        var mapFile = Resources.Load(mapName);
        return mapFile.ToString();
    }


    //json serialization stuff
    [System.Serializable]
    public class FSMap
    {
        public List<MapAsset> assets;
    }

    [System.Serializable]
    public class MapAsset
    {
        public string n;
        public List<float> p;
        public List<float> o;
        public List<float> s;
        public MapAssetMetadata m;
    }

    [System.Serializable]
    public class MapAssetMetadata
    {
        public int id;
        public int? checkpoint_order;
        public bool? lap_timer;
    }
}
