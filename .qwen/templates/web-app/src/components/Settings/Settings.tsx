import React, { useState } from 'react'
import styled from 'styled-components'

// Qwen-optimized: TypeScript interfaces for settings
interface AppSettings {
  theme: 'light' | 'dark' | 'auto'
  language: string
  notifications: boolean
  aiModel: string
  apiKey: string
  maxTokens: number
  temperature: number
}

interface SettingSection {
  title: string
  description: string
  settings: SettingItem[]
}

interface SettingItem {
  id: string
  label: string
  description: string
  type: 'toggle' | 'select' | 'input' | 'slider'
  value: any
  options?: string[]
}

// Qwen-optimized: Custom hook for settings management
const useSettings = () => {
  const [settings, setSettings] = useState<AppSettings>({
    theme: 'auto',
    language: 'en',
    notifications: true,
    aiModel: 'qwen-turbo',
    apiKey: '',
    maxTokens: 2048,
    temperature: 0.7
  })

  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  const updateSetting = <K extends keyof AppSettings>(key: K, value: AppSettings[K]) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  const saveSettings = async () => {
    setIsLoading(true)
    setMessage(null)

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))

      // In a real app, this would save to backend/localStorage
      localStorage.setItem('qwen-settings', JSON.stringify(settings))

      setMessage({ type: 'success', text: 'Settings saved successfully!' })

      // Clear message after 3 seconds
      setTimeout(() => setMessage(null), 3000)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to save settings. Please try again.' })
    } finally {
      setIsLoading(false)
    }
  }

  const loadSettings = () => {
    try {
      const saved = localStorage.getItem('qwen-settings')
      if (saved) {
        setSettings(JSON.parse(saved))
        setMessage({ type: 'success', text: 'Settings loaded from local storage.' })
        setTimeout(() => setMessage(null), 2000)
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to load settings.' })
    }
  }

  return {
    settings,
    updateSetting,
    saveSettings,
    loadSettings,
    isLoading,
    message
  }
}

// Qwen-optimized: Styled components for settings UI
const SettingsContainer = styled.div`
  color: white;
  max-width: 800px;
  margin: 0 auto;
`

const SettingsHeader = styled.div`
  text-align: center;
  margin-bottom: 3rem;
`

const SettingsTitle = styled.h2`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #fff 0%, #a8edea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`

const SettingsDescription = styled.p`
  opacity: 0.8;
  font-size: 1.1rem;
  line-height: 1.6;
`

const SettingsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
`

const SettingsSection = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
`

const SectionHeader = styled.div`
  margin-bottom: 2rem;
`

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
`

const SectionDescription = styled.p`
  opacity: 0.7;
  font-size: 0.9rem;
  line-height: 1.5;
`

const SettingRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  &:last-child {
    border-bottom: none;
  }

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
`

const SettingInfo = styled.div`
  flex: 1;
`

const SettingLabel = styled.div`
  font-weight: 500;
  margin-bottom: 0.25rem;
`

const SettingDescription = styled.div`
  font-size: 0.9rem;
  opacity: 0.7;
  line-height: 1.4;
`

const SettingControl = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`

const Toggle = styled.label`
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;

  input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  span {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: ${props => props.checked ? '#4ade80' : 'rgba(255, 255, 255, 0.3)'};
    transition: 0.4s;
    border-radius: 34px;

    &::before {
      position: absolute;
      content: "";
      height: 26px;
      width: 26px;
      left: 4px;
      bottom: 4px;
      background-color: white;
      transition: 0.4s;
      border-radius: 50%;
      transform: ${props => props.checked ? 'translateX(26px)' : 'translateX(0)'};
    }
  }
`

const Select = styled.select`
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.9rem;
  min-width: 150px;

  option {
    background: #2d3748;
    color: white;
  }
`

const Input = styled.input`
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.9rem;
  min-width: 200px;

  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }
`

const Slider = styled.input`
  width: 100px;
  height: 6px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.3);
  outline: none;
  -webkit-appearance: none;

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    cursor: pointer;
  }

  &::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    cursor: pointer;
    border: none;
  }
`

const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: center;
`

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  ${props => props.variant === 'primary' ? `
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
  ` : `
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);

    &:hover {
      background: rgba(255, 255, 255, 0.2);
    }
  `}
`

const Message = styled.div<{ type: 'success' | 'error' }>`
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  background: ${props => props.type === 'success' ? 'rgba(74, 222, 128, 0.2)' : 'rgba(239, 68, 68, 0.2)'};
  color: ${props => props.type === 'success' ? '#4ade80' : '#ef4444'};
  border: 1px solid ${props => props.type === 'success' ? 'rgba(74, 222, 128, 0.3)' : 'rgba(239, 68, 68, 0.3)'};
`

const Settings: React.FC = () => {
  const { settings, updateSetting, saveSettings, loadSettings, isLoading, message } = useSettings()

  return (
    <SettingsContainer>
      <SettingsHeader>
        <SettingsTitle>⚙️ Settings</SettingsTitle>
        <SettingsDescription>
          Configure your Qwen Web App preferences and AI model settings
        </SettingsDescription>
      </SettingsHeader>

      {message && <Message type={message.type}>{message.text}</Message>}

      <SettingsGrid>
        <SettingsSection>
          <SectionHeader>
            <SectionTitle>Appearance</SectionTitle>
            <SectionDescription>
              Customize the look and feel of your application
            </SectionDescription>
          </SectionHeader>

          <SettingRow>
            <SettingInfo>
              <SettingLabel>Theme</SettingLabel>
              <SettingDescription>
                Choose your preferred color scheme
              </SettingDescription>
            </SettingInfo>
            <SettingControl>
              <Select
                value={settings.theme}
                onChange={(e) => updateSetting('theme', e.target.value as AppSettings['theme'])}
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="auto">Auto</option>
              </Select>
            </SettingControl>
          </SettingRow>

          <SettingRow>
            <SettingInfo>
              <SettingLabel>Language</SettingLabel>
              <SettingDescription>
                Select your preferred language
              </SettingDescription>
            </SettingInfo>
            <SettingControl>
              <Select
                value={settings.language}
                onChange={(e) => updateSetting('language', e.target.value)}
              >
                <option value="en">English</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
                <option value="zh">中文</option>
              </Select>
            </SettingControl>
          </SettingRow>
        </SettingsSection>

        <SettingsSection>
          <SectionHeader>
            <SectionTitle>Notifications</SectionTitle>
            <SectionDescription>
              Manage how you receive notifications
            </SectionDescription>
          </SectionHeader>

          <SettingRow>
            <SettingInfo>
              <SettingLabel>Enable Notifications</SettingLabel>
              <SettingDescription>
                Receive notifications for important updates
              </SettingDescription>
            </SettingInfo>
            <SettingControl>
              <Toggle checked={settings.notifications}>
                <input
                  type="checkbox"
                  checked={settings.notifications}
                  onChange={(e) => updateSetting('notifications', e.target.checked)}
                />
                <span />
              </Toggle>
            </SettingControl>
          </SettingRow>
        </SettingsSection>

        <SettingsSection>
          <SectionHeader>
            <SectionTitle>AI Configuration</SectionTitle>
            <SectionDescription>
              Configure your Qwen AI model settings
            </SectionDescription>
          </SectionHeader>

          <SettingRow>
            <SettingInfo>
              <SettingLabel>AI Model</SettingLabel>
              <SettingDescription>
                Select the Qwen model to use for AI interactions
              </SettingDescription>
            </SettingInfo>
            <SettingControl>
              <Select
                value={settings.aiModel}
                onChange={(e) => updateSetting('aiModel', e.target.value)}
              >
                <option value="qwen-turbo">Qwen Turbo</option>
                <option value="qwen-plus">Qwen Plus</option>
                <option value="qwen-max">Qwen Max</option>
              </Select>
            </SettingControl>
          </SettingRow>

          <SettingRow>
            <SettingInfo>
              <SettingLabel>API Key</SettingLabel>
              <SettingDescription>
                Your Qwen API key for authentication
              </SettingDescription>
            </SettingInfo>
            <SettingControl>
              <Input
                type="password"
                placeholder="Enter your API key"
                value={settings.apiKey}
                onChange={(e) => updateSetting('apiKey', e.target.value)}
              />
            </SettingControl>
          </SettingRow>

          <SettingRow>
            <SettingInfo>
              <SettingLabel>Max Tokens</SettingLabel>
              <SettingDescription>
                Maximum number of tokens per response
              </SettingDescription>
            </SettingInfo>
            <SettingControl>
              <Input
                type="number"
                min="100"
                max="8192"
                value={settings.maxTokens}
                onChange={(e) => updateSetting('maxTokens', parseInt(e.target.value))}
              />
            </SettingControl>
          </SettingRow>

          <SettingRow>
            <SettingInfo>
              <SettingLabel>Temperature</SettingLabel>
              <SettingDescription>
                Controls randomness in AI responses (0.0 - 1.0)
              </SettingDescription>
            </SettingInfo>
            <SettingControl>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <Slider
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={settings.temperature}
                  onChange={(e) => updateSetting('temperature', parseFloat(e.target.value))}
                />
                <span style={{ minWidth: '40px', fontSize: '0.9rem' }}>
                  {settings.temperature}
                </span>
              </div>
            </SettingControl>
          </SettingRow>
        </SettingsSection>
      </SettingsGrid>

      <ButtonGroup>
        <Button variant="secondary" onClick={loadSettings}>
          Load Settings
        </Button>
        <Button
          variant="primary"
          onClick={saveSettings}
          disabled={isLoading}
        >
          {isLoading ? 'Saving...' : 'Save Settings'}
        </Button>
      </ButtonGroup>
    </SettingsContainer>
  )
}

export default Settings