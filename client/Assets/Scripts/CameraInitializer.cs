using UnityEngine;
using System.Collections;

public class CameraInitializer : MonoBehaviour {

	void Start () {
	    // camera
        bool focusModeSet = CameraDevice.Instance.SetFocusMode(CameraDevice.FocusMode.FOCUS_MODE_CONTINUOUSAUTO);
        if (!focusModeSet)
        {
            Debug.Log("Failed to set focus mode (unsupported mode).");
        }
	}
}
