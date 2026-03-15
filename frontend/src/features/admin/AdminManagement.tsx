import { useState, useEffect } from 'react';
import {
    Box, Flex, Text, Button, Tabs, TabList, Tab, TabPanels, TabPanel,
    VStack, HStack, Badge, Input, Textarea, FormControl, FormLabel,
    useToast, Table, Thead, Tbody, Tr, Th, Td, IconButton,
    Divider, Grid, Card, CardBody, Switch
} from '@chakra-ui/react';
import { FiSave, FiRefreshCw, FiPlus, FiTrash2, FiSettings, FiMessageSquare } from 'react-icons/fi';

export function AdminManagement() {
    const [agents, setAgents] = useState([
        { id: '1', nome: 'Bella Suporte', departamento: 'suporte', contexto: 'Você ajuda em dúvidas técnicas...', active: true },
        { id: '2', nome: 'Bella Vendas', departamento: 'vendas', contexto: 'Você foca em fechar pedidos...', active: true }
    ]);

    const [instances, setInstances] = useState([
        { name: 'Global_Main', status: 'connected', owner: 'BellaZap Admin' },
        { name: 'Rev_01_Mark', status: 'disconnected', owner: 'Mark Representante' }
    ]);

    const toast = useToast();

    const handleSaveAgent = (id: string) => {
        toast({ title: 'Configuração salva', status: 'success', duration: 2000 });
    };

    return (
        <Box p={8} bg="gray.50" minH="100vh">
            <Flex justifyContent="space-between" alignItems="center" mb={10}>
                <Box>
                    <Text fontSize="2xl" fontWeight="bold" color="blue.900">Gestão Estratégica & SaaS</Text>
                    <Text color="gray.600">Configure seus agentes IA e instâncias de WhatsApp centralizadas.</Text>
                </Box>
                <HStack spacing={4}>
                    <Button leftIcon={<FiRefreshCw />} variant="ghost">Sincronizar Tudo</Button>
                    <Button colorScheme="blue" leftIcon={<FiPlus />}>Novo Agente</Button>
                </HStack>
            </Flex>

            <Tabs variant="soft-rounded" colorScheme="blue">
                <TabList bg="white" p={2} borderRadius="full" shadow="sm" mb={8}>
                    <Tab><FiSettings style={{ marginRight: '8px' }} /> Configurações de Agentes</Tab>
                    <Tab><FiMessageSquare style={{ marginRight: '8px' }} /> Instâncias Evolution API</Tab>
                    <Tab>Monitoramento SaaS</Tab>
                </TabList>

                <TabPanels>
                    {/* Aba de Agentes */}
                    <TabPanel>
                        <Grid templateColumns="repeat(auto-fit, minmax(400px, 1fr))" gap={6}>
                            {agents.map(agent => (
                                <Card key={agent.id} borderRadius="xl" shadow="sm" border="1px" borderColor="gray.100">
                                    <CardBody>
                                        <Flex justifyContent="space-between" mb={4}>
                                            <VStack align="start" spacing={0}>
                                                <Text fontWeight="bold" fontSize="lg">{agent.nome}</Text>
                                                <Badge colorScheme="purple">{agent.departamento.toUpperCase()}</Badge>
                                            </VStack>
                                            <Switch defaultChecked={agent.active} colorScheme="green" />
                                        </Flex>

                                        <VStack spacing={4}>
                                            <FormControl>
                                                <FormLabel fontSize="sm" color="gray.600">Contexto Estratégico (Prompt de Sistema)</FormLabel>
                                                <Textarea
                                                    defaultValue={agent.contexto}
                                                    h="120px"
                                                    borderRadius="md"
                                                    fontSize="sm"
                                                    focusBorderColor="blue.400"
                                                />
                                            </FormControl>

                                            <HStack w="100%" justifyContent="space-between">
                                                <Button size="sm" variant="outline" leftIcon={<FiTrash2 />} colorScheme="red">Remover</Button>
                                                <Button size="sm" colorScheme="blue" leftIcon={<FiSave />} onClick={() => handleSaveAgent(agent.id)}>Salvar Alterações</Button>
                                            </HStack>
                                        </VStack>
                                    </CardBody>
                                </Card>
                            ))}
                        </Grid>
                    </TabPanel>

                    {/* Aba de Instâncias WhatsApp */}
                    <TabPanel>
                        <Box bg="white" borderRadius="xl" shadow="sm" overflow="hidden">
                            <Table variant="simple">
                                <Thead bg="gray.50">
                                    <Tr>
                                        <Th>Nome da Instância</Th>
                                        <Th>Responsável</Th>
                                        <Th>Status de Conexão</Th>
                                        <Th textAlign="right">Ações</Th>
                                    </Tr>
                                </Thead>
                                <Tbody>
                                    {instances.map(inst => (
                                        <Tr key={inst.name}>
                                            <Td fontWeight="medium">{inst.name}</Td>
                                            <Td>{inst.owner}</Td>
                                            <Td>
                                                <Badge colorScheme={inst.status === 'connected' ? 'green' : 'red'}>
                                                    {inst.status.toUpperCase()}
                                                </Badge>
                                            </Td>
                                            <Td textAlign="right">
                                                <HStack justifyContent="flex-end">
                                                    <Button size="xs" colorScheme="blue" variant="outline">Consultar QR</Button>
                                                    <Button size="xs" colorScheme="red" variant="ghost">Desconectar</Button>
                                                    <IconButton aria-label="Settings" icon={<FiSettings />} size="xs" variant="ghost" />
                                                </HStack>
                                            </Td>
                                        </Tr>
                                    ))}
                                </Tbody>
                            </Table>
                        </Box>
                    </TabPanel>

                    {/* Monitoramento SaaS */}
                    <TabPanel>
                        <VStack spacing={6} align="stretch">
                            <Card bg="blue.900" color="white" borderRadius="xl">
                                <CardBody>
                                    <Grid templateColumns="repeat(3, 1fr)" gap={10}>
                                        <Box>
                                            <Text fontSize="sm" opacity={0.8}>BD Status</Text>
                                            <Text fontSize="xl" fontWeight="bold">Healthy (v15.2)</Text>
                                        </Box>
                                        <Box>
                                            <Text fontSize="sm" opacity={0.8}>Celery Workers</Text>
                                            <Text fontSize="xl" fontWeight="bold">3 Ativos</Text>
                                        </Box>
                                        <Box>
                                            <Text fontSize="sm" opacity={0.8}>Storage</Text>
                                            <Text fontSize="xl" fontWeight="bold">42% utilizado</Text>
                                        </Box>
                                    </Grid>
                                </CardBody>
                            </Card>
                        </VStack>
                    </TabPanel>
                </TabPanels>
            </Tabs>
        </Box>
    );
}
