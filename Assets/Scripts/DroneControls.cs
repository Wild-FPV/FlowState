// GENERATED AUTOMATICALLY FROM 'Assets/Scripts/DroneControls.inputactions'

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Utilities;

public class @DroneControls : IInputActionCollection, IDisposable
{
    public InputActionAsset asset { get; }
    public @DroneControls()
    {
        asset = InputActionAsset.FromJson(@"{
    ""name"": ""DroneControls"",
    ""maps"": [
        {
            ""name"": ""Armed"",
            ""id"": ""d4b4ddef-64a1-4c34-be7d-3ecfce3582dc"",
            ""actions"": [
                {
                    ""name"": ""Throttle"",
                    ""type"": ""PassThrough"",
                    ""id"": ""9fcf0596-768d-4ce4-a438-2d465b4feb5e"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                },
                {
                    ""name"": ""Yaw"",
                    ""type"": ""PassThrough"",
                    ""id"": ""39f2f8ca-e3fb-4b99-9ff0-a86cddd1b830"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                },
                {
                    ""name"": ""Roll"",
                    ""type"": ""PassThrough"",
                    ""id"": ""b75fa9e0-ae2f-4ed6-8011-381a731178e5"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                },
                {
                    ""name"": ""Pitch"",
                    ""type"": ""PassThrough"",
                    ""id"": ""d970d0c5-9567-458a-bde3-00bf44839aad"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                }
            ],
            ""bindings"": [
                {
                    ""name"": """",
                    ""id"": ""c6ad7a04-ab17-4a6b-b473-a27d62b2f063"",
                    ""path"": ""<HID::Team-BlackSheep TBS Joystick>/stick/x"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Throttle"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""79b549fc-fb95-4ed1-9c76-96ea9d6240a2"",
                    ""path"": ""<HID::Team-BlackSheep TBS Joystick>/rx"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Yaw"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""59d9fcd3-b380-483a-89d6-e384b85da121"",
                    ""path"": ""<Joystick>/stick/y"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Roll"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""559930e3-2f38-47dc-8271-11cea0d036d7"",
                    ""path"": ""<HID::Team-BlackSheep TBS Joystick>/z"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Pitch"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                }
            ]
        }
    ],
    ""controlSchemes"": [
        {
            ""name"": ""New control scheme"",
            ""bindingGroup"": ""New control scheme"",
            ""devices"": []
        }
    ]
}");
        // Armed
        m_Armed = asset.FindActionMap("Armed", throwIfNotFound: true);
        m_Armed_Throttle = m_Armed.FindAction("Throttle", throwIfNotFound: true);
        m_Armed_Yaw = m_Armed.FindAction("Yaw", throwIfNotFound: true);
        m_Armed_Roll = m_Armed.FindAction("Roll", throwIfNotFound: true);
        m_Armed_Pitch = m_Armed.FindAction("Pitch", throwIfNotFound: true);
    }

    public void Dispose()
    {
        UnityEngine.Object.Destroy(asset);
    }

    public InputBinding? bindingMask
    {
        get => asset.bindingMask;
        set => asset.bindingMask = value;
    }

    public ReadOnlyArray<InputDevice>? devices
    {
        get => asset.devices;
        set => asset.devices = value;
    }

    public ReadOnlyArray<InputControlScheme> controlSchemes => asset.controlSchemes;

    public bool Contains(InputAction action)
    {
        return asset.Contains(action);
    }

    public IEnumerator<InputAction> GetEnumerator()
    {
        return asset.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }

    public void Enable()
    {
        asset.Enable();
    }

    public void Disable()
    {
        asset.Disable();
    }

    // Armed
    private readonly InputActionMap m_Armed;
    private IArmedActions m_ArmedActionsCallbackInterface;
    private readonly InputAction m_Armed_Throttle;
    private readonly InputAction m_Armed_Yaw;
    private readonly InputAction m_Armed_Roll;
    private readonly InputAction m_Armed_Pitch;
    public struct ArmedActions
    {
        private @DroneControls m_Wrapper;
        public ArmedActions(@DroneControls wrapper) { m_Wrapper = wrapper; }
        public InputAction @Throttle => m_Wrapper.m_Armed_Throttle;
        public InputAction @Yaw => m_Wrapper.m_Armed_Yaw;
        public InputAction @Roll => m_Wrapper.m_Armed_Roll;
        public InputAction @Pitch => m_Wrapper.m_Armed_Pitch;
        public InputActionMap Get() { return m_Wrapper.m_Armed; }
        public void Enable() { Get().Enable(); }
        public void Disable() { Get().Disable(); }
        public bool enabled => Get().enabled;
        public static implicit operator InputActionMap(ArmedActions set) { return set.Get(); }
        public void SetCallbacks(IArmedActions instance)
        {
            if (m_Wrapper.m_ArmedActionsCallbackInterface != null)
            {
                @Throttle.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnThrottle;
                @Throttle.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnThrottle;
                @Throttle.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnThrottle;
                @Yaw.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnYaw;
                @Yaw.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnYaw;
                @Yaw.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnYaw;
                @Roll.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnRoll;
                @Roll.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnRoll;
                @Roll.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnRoll;
                @Pitch.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnPitch;
                @Pitch.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnPitch;
                @Pitch.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnPitch;
            }
            m_Wrapper.m_ArmedActionsCallbackInterface = instance;
            if (instance != null)
            {
                @Throttle.started += instance.OnThrottle;
                @Throttle.performed += instance.OnThrottle;
                @Throttle.canceled += instance.OnThrottle;
                @Yaw.started += instance.OnYaw;
                @Yaw.performed += instance.OnYaw;
                @Yaw.canceled += instance.OnYaw;
                @Roll.started += instance.OnRoll;
                @Roll.performed += instance.OnRoll;
                @Roll.canceled += instance.OnRoll;
                @Pitch.started += instance.OnPitch;
                @Pitch.performed += instance.OnPitch;
                @Pitch.canceled += instance.OnPitch;
            }
        }
    }
    public ArmedActions @Armed => new ArmedActions(this);
    private int m_NewcontrolschemeSchemeIndex = -1;
    public InputControlScheme NewcontrolschemeScheme
    {
        get
        {
            if (m_NewcontrolschemeSchemeIndex == -1) m_NewcontrolschemeSchemeIndex = asset.FindControlSchemeIndex("New control scheme");
            return asset.controlSchemes[m_NewcontrolschemeSchemeIndex];
        }
    }
    public interface IArmedActions
    {
        void OnThrottle(InputAction.CallbackContext context);
        void OnYaw(InputAction.CallbackContext context);
        void OnRoll(InputAction.CallbackContext context);
        void OnPitch(InputAction.CallbackContext context);
    }
}
