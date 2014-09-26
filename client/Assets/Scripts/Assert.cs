using UnityEngine;
using System.Collections;

namespace marika
{
    public class Assert
    {
        [System.Diagnostics.Conditional("UNITY_EDITOR")]
        public static void Test(bool comparison, string message)
        {
            if (!comparison)
            {
                Debug.LogWarning(message);
                Debug.Break();
            }
        }

        [System.Diagnostics.Conditional("UNITY_EDITOR")]
        public static void Test(bool comparison)
        {
            Test(comparison, "Assert Occur");
        }


        [System.Diagnostics.Conditional("UNITY_EDITOR")]
        public static void Throw(string message)
        {
            Debug.LogWarning(message);
        }

    }
}