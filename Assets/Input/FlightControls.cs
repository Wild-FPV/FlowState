// GENERATED AUTOMATICALLY FROM 'Assets/Input/FlightControls.inputactions'

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Utilities;

public class @FlightControls : IInputActionCollection, IDisposable
{
    public InputActionAsset asset { get; }
    public @FlightControls()
    {
        asset = InputActionAsset.FromJson(@"{
    ""name"": ""FlightControls"",
    ""maps"": [
        {
            ""name"": ""Armed"",
            ""id"": ""2d12fbcb-e43d-4c3d-8d45-f278b37deea6"",
            ""actions"": [
                {
                    ""name"": ""Throttle"",
                    ""type"": ""Value"",
                    ""id"": ""44206c51-771f-4e82-a3d5-ce427aca27f8"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                },
                {
                    ""name"": ""Pitch"",
                    ""type"": ""Value"",
                    ""id"": ""2129194c-032f-4052-a4b2-e715ad24e3ad"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                },
                {
                    ""name"": ""Roll"",
                    ""type"": ""Value"",
                    ""id"": ""313d6939-dccf-4484-850b-6f5edde11d21"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                },
                {
                    ""name"": ""Yaw"",
                    ""type"": ""Value"",
                    ""id"": ""c2fd8a90-ad1c-456a-9e45-1e7b08484ddb"",
                    ""expectedControlType"": ""Axis"",
                    ""processors"": """",
                    ""interactions"": """"
                },
                {
                    ""name"": ""Menu"",
                    ""type"": ""Button"",
                    ""id"": ""be5b5290-0311-4b7a-a039-f186af013725"",
                    ""expectedControlType"": ""Button"",
                    ""processors"": """",
                    ""interactions"": """"
                }
            ],
            ""bindings"": [
                {
                    ""name"": """",
                    ""id"": ""9c8b0c69-6790-4d77-89a7-faf695854ea1"",
                    ""path"": ""<Joystick>/stick/x"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": ""Joystick"",
                    ""action"": ""Throttle"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""786e0482-5e36-4e94-bbb8-f7959e984f6f"",
                    ""path"": ""<Gamepad>/rightStick/y"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Throttle"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""3d650cd0-1046-4f6b-94b5-4712caf97c84"",
                    ""path"": ""<Joystick>/z"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Pitch"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""0bc14e10-729c-49eb-bd6c-f15a940934e4"",
                    ""path"": ""<Gamepad>/leftStick/y"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Pitch"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""7bf43509-4dfb-4b30-8159-c59cbbab444c"",
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
                    ""id"": ""9efab0f1-44db-45dc-b50f-6bfe465b7b3a"",
                    ""path"": ""<Gamepad>/leftStick/x"",
                    ""interactions"": """",
                    ""processors"": ""Invert"",
                    ""groups"": """",
                    ""action"": ""Roll"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""e5fce8da-6169-43c3-875d-8570df2d3017"",
                    ""path"": ""<Joystick>/rx"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Yaw"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                },
                {
                    ""name"": """",
                    ""id"": ""5a6e2fa1-6d0f-4a67-82ce-f8185152a412"",
                    ""path"": ""<Gamepad>/rightStick/x"",
                    ""interactions"": """",
                    ""processors"": """",
                    ""groups"": """",
                    ""action"": ""Yaw"",
                    ""isComposite"": false,
                    ""isPartOfComposite"": false
                }
            ]
        }
    ],
    ""controlSchemes"": [
        {
            ""name"": ""Keyboard&Mouse"",
            ""bindingGroup"": ""Keyboard&Mouse"",
            ""devices"": [
                {
                    ""devicePath"": ""<Keyboard>"",
                    ""isOptional"": false,
                    ""isOR"": false
                },
                {
                    ""devicePath"": ""<Mouse>"",
                    ""isOptional"": false,
                    ""isOR"": false
                }
            ]
        },
        {
            ""name"": ""Gamepad"",
            ""bindingGroup"": ""Gamepad"",
            ""devices"": [
                {
                    ""devicePath"": ""<Gamepad>"",
                    ""isOptional"": false,
                    ""isOR"": false
                }
            ]
        },
        {
            ""name"": ""Touch"",
            ""bindingGroup"": ""Touch"",
            ""devices"": [
                {
                    ""devicePath"": ""<Touchscreen>"",
                    ""isOptional"": false,
                    ""isOR"": false
                }
            ]
        },
        {
            ""name"": ""Joystick"",
            ""bindingGroup"": ""Joystick"",
            ""devices"": [
                {
                    ""devicePath"": ""<Joystick>"",
                    ""isOptional"": false,
                    ""isOR"": false
                }
            ]
        },
        {
            ""name"": ""XR"",
            ""bindingGroup"": ""XR"",
            ""devices"": [
                {
                    ""devicePath"": ""<XRController>"",
                    ""isOptional"": false,
                    ""isOR"": false
                }
            ]
        }
    ]
}");
        // Armed
        m_Armed = asset.FindActionMap("Armed", throwIfNotFound: true);
        m_Armed_Throttle = m_Armed.FindAction("Throttle", throwIfNotFound: true);
        m_Armed_Pitch = m_Armed.FindAction("Pitch", throwIfNotFound: true);
        m_Armed_Roll = m_Armed.FindAction("Roll", throwIfNotFound: true);
        m_Armed_Yaw = m_Armed.FindAction("Yaw", throwIfNotFound: true);
        m_Armed_Menu = m_Armed.FindAction("Menu", throwIfNotFound: true);
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
    private readonly InputAction m_Armed_Pitch;
    private readonly InputAction m_Armed_Roll;
    private readonly InputAction m_Armed_Yaw;
    private readonly InputAction m_Armed_Menu;
    public struct ArmedActions
    {
        private @FlightControls m_Wrapper;
        public ArmedActions(@FlightControls wrapper) { m_Wrapper = wrapper; }
        public InputAction @Throttle => m_Wrapper.m_Armed_Throttle;
        public InputAction @Pitch => m_Wrapper.m_Armed_Pitch;
        public InputAction @Roll => m_Wrapper.m_Armed_Roll;
        public InputAction @Yaw => m_Wrapper.m_Armed_Yaw;
        public InputAction @Menu => m_Wrapper.m_Armed_Menu;
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
                @Pitch.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnPitch;
                @Pitch.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnPitch;
                @Pitch.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnPitch;
                @Roll.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnRoll;
                @Roll.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnRoll;
                @Roll.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnRoll;
                @Yaw.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnYaw;
                @Yaw.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnYaw;
                @Yaw.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnYaw;
                @Menu.started -= m_Wrapper.m_ArmedActionsCallbackInterface.OnMenu;
                @Menu.performed -= m_Wrapper.m_ArmedActionsCallbackInterface.OnMenu;
                @Menu.canceled -= m_Wrapper.m_ArmedActionsCallbackInterface.OnMenu;
            }
            m_Wrapper.m_ArmedActionsCallbackInterface = instance;
            if (instance != null)
            {
                @Throttle.started += instance.OnThrottle;
                @Throttle.performed += instance.OnThrottle;
                @Throttle.canceled += instance.OnThrottle;
                @Pitch.started += instance.OnPitch;
                @Pitch.performed += instance.OnPitch;
                @Pitch.canceled += instance.OnPitch;
                @Roll.started += instance.OnRoll;
                @Roll.performed += instance.OnRoll;
                @Roll.canceled += instance.OnRoll;
                @Yaw.started += instance.OnYaw;
                @Yaw.performed += instance.OnYaw;
                @Yaw.canceled += instance.OnYaw;
                @Menu.started += instance.OnMenu;
                @Menu.performed += instance.OnMenu;
                @Menu.canceled += instance.OnMenu;
            }
        }
    }
    public ArmedActions @Armed => new ArmedActions(this);
    private int m_KeyboardMouseSchemeIndex = -1;
    public InputControlScheme KeyboardMouseScheme
    {
        get
        {
            if (m_KeyboardMouseSchemeIndex == -1) m_KeyboardMouseSchemeIndex = asset.FindControlSchemeIndex("Keyboard&Mouse");
            return asset.controlSchemes[m_KeyboardMouseSchemeIndex];
        }
    }
    private int m_GamepadSchemeIndex = -1;
    public InputControlScheme GamepadScheme
    {
        get
        {
            if (m_GamepadSchemeIndex == -1) m_GamepadSchemeIndex = asset.FindControlSchemeIndex("Gamepad");
            return asset.controlSchemes[m_GamepadSchemeIndex];
        }
    }
    private int m_TouchSchemeIndex = -1;
    public InputControlScheme TouchScheme
    {
        get
        {
            if (m_TouchSchemeIndex == -1) m_TouchSchemeIndex = asset.FindControlSchemeIndex("Touch");
            return asset.controlSchemes[m_TouchSchemeIndex];
        }
    }
    private int m_JoystickSchemeIndex = -1;
    public InputControlScheme JoystickScheme
    {
        get
        {
            if (m_JoystickSchemeIndex == -1) m_JoystickSchemeIndex = asset.FindControlSchemeIndex("Joystick");
            return asset.controlSchemes[m_JoystickSchemeIndex];
        }
    }
    private int m_XRSchemeIndex = -1;
    public InputControlScheme XRScheme
    {
        get
        {
            if (m_XRSchemeIndex == -1) m_XRSchemeIndex = asset.FindControlSchemeIndex("XR");
            return asset.controlSchemes[m_XRSchemeIndex];
        }
    }
    public interface IArmedActions
    {
        void OnThrottle(InputAction.CallbackContext context);
        void OnPitch(InputAction.CallbackContext context);
        void OnRoll(InputAction.CallbackContext context);
        void OnYaw(InputAction.CallbackContext context);
        void OnMenu(InputAction.CallbackContext context);
    }
}
