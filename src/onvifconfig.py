from time import sleep
from onvif import ONVIFCamera

class ptzcam():
    def __init__(self, ip, port, user, password, wsdl):
        # file = open('./preset.txt', 'r')
        print('IP camera initialization')

        self.mycam = ONVIFCamera(ip, port, user, password, wsdl)
        print('Connected to ONVIF camera')

        # Create media service object
        self.media = self.mycam.create_media_service()
        print('Created media service object')

        # Get target profile
        self.media_profile = self.media.GetProfiles()[0]
        # Use the first profile and Profiles have at least one
        token = self.media_profile.token

        #PTZ controls  -------------------------------------------------------------
        # Create ptz service object
        print('Creating PTZ object')
        self.ptz = self.mycam.create_ptz_service()
        print('Created PTZ service object')

        #Get available PTZ services
        request = self.ptz.create_type('GetServiceCapabilities')
        Service_Capabilities = self.ptz.GetServiceCapabilities(request)
        print('PTZ service capabilities:')

        #Get PTZ status
        status = self.ptz.GetStatus({'ProfileToken':token})

        # Get PTZ configuration options for getting option ranges
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self.media_profile.PTZConfiguration.token
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)

        self.requestc = self.ptz.create_type('ContinuousMove')
        self.requestc.ProfileToken = self.media_profile.token

        self.requests = self.ptz.create_type('Stop')
        self.requests.ProfileToken = self.media_profile.token

        self.requestp = self.ptz.create_type('SetPreset')
        self.requestp.ProfileToken = self.media_profile.token

        self.requestg = self.ptz.create_type('GotoPreset')
        self.requestg.ProfileToken = self.media_profile.token

        self.requestrp = self.ptz.create_type('RemovePreset')
        self.requestrp.ProfileToken = self.media_profile.token
        
        # Get PTZ Presets
        self.ptzPresetsList = self.ptz.GetPresets(self.media_profile.token)
        print('Got preset:')
        print(self.ptzPresetsList)
        print('====================================')

        self.stop()

    #Stop pan, tilt and zoom
    def stop(self):
        self.requests.PanTilt = True
        self.requests.Zoom = True
        print ('Stop:')
        print
        self.ptz.Stop(self.requests)
        print ('Stopped')

    #Continuous move functions
    def perform_move(self, timeout):
        # Start continuous move
        ret = self.ptz.ContinuousMove(self.requestc)
        print ('Continuous move completed', ret)
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        self.stop()
        sleep(2)
        print

    def move_tilt(self, velocity, timeout):
        print('Move tilt...', velocity)
        # self.requestc.Velocity.PanTilt.x = 0.0
        self.requestc.Velocity={'PanTilt':{'x':0.0,'y':velocity}}
        # self.requestc.Velocity.PanTilt.y = velocity
        self.perform_move(timeout)

    def move_pan(self, velocity, timeout):
        print('Move pan...', velocity)
        # self.requestc.Velocity.PanTilt.x = velocity
        # self.requestc.Velocity.PanTilt.y = 0.0
        self.requestc.Velocity={'PanTilt':{'x':velocity,'y':0.0}}
        self.perform_move(timeout)

    def update_list(self):
        self.ptzPresetsList = self.ptz.GetPresets(self.requestc.ProfileToken)

    def set_preset(self, name):
        print("========================================")
        print('Set Preset')
        PresetNameList = list(item['Name'] for item in self.ptzPresetsList if item['Name'] == str(name))
        print(PresetNameList)
        if name not in PresetNameList: 
            self.requestp.PresetName = name
            # self.requestp.PresetToken = 'PRESET_'+str(number)
            self.preset = self.ptz.SetPreset(self.requestp)  #returns the PresetTokens
            print('Set Preset:')
            print(self.preset)
            self.update_list()
        else:
            print('Already have Preset')
        sleep(1)

    def get_preset(self):
        print("========================================")
        print('Got preset:')
        print(self.ptzPresetsList)
        sleep(1)

    def goto_preset(self, name):
        print("========================================")
        PresetNameList = list(item['Name'] for item in self.ptzPresetsList if item['Name'] == str(name))
        if name in PresetNameList: 
            preset_arg = next(item for item in self.ptzPresetsList if item['Name'] == str(name))
            self.requestg.PresetToken = preset_arg.token
            self.ptz.GotoPreset(self.requestg)
            print ('Going to Preset:')
            print (name)
        else:
            print('You not have any Preset')
        sleep(2)
    
    def remove_preset(self):
        print("========================================")
        print('Remove Preset')
        if len(self.ptzPresetsList) > 0:
            for item in self.ptzPresetsList:
                self.requestrp.PresetToken = item.token
                self.ptz.RemovePreset(self.requestrp)
                print('Remove Successfully')
                self.update_list()
        else:
            print('You not have any Preset')
        sleep(2)
        
    def current_loc(self):        
        status = self.ptz.GetStatus(self.media_profile.token)
        print ('PTZ status:')
        print ('Pan position:', status.Position.PanTilt.x)
        print ('Tilt position:', status.Position.PanTilt.y)
        print ('Zoom position:', status.Position.Zoom.x)
        print ('Pan/Tilt Moving?:', status.MoveStatus.PanTilt)
        return status.Position.PanTilt.x, status.Position.PanTilt.y, status.Position.Zoom.x, status.MoveStatus.PanTilt
    
    def position_initial(self, x, y, Zoom, PanTilt) :
        print("Coming back at the position of the beginning")
        self.requesta.Position.PanTilt.x = x
        self.requesta.Position.PanTilt.y = y
        ret = self.ptz.AbsoluteMove(self.requesta)
        print ('Absolute move completed')