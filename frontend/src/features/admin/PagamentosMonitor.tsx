import { useState, useEffect } from 'react';
import {
  Box, Grid, Stat, StatLabel, StatNumber, StatHelpText,
  Table, Thead, Tbody, Tr, Th, Td, Badge, Button,
  useToast, Alert, AlertIcon, AlertTitle, AlertDescription
} from '@chakra-ui/react';
// import { api } from '@/core/api/client'; 

export function PagamentosMonitor() {
  const [providers, setProviders] = useState([
    { id: '1', name: 'asaas', healthy: true, current_provider: 'asaas', fallback_count: 0 },
    { id: '2', name: 'abacate', healthy: true, current_provider: 'asaas', fallback_count: 5 }
  ]);
  const [transacoesPendentes, setTransacoesPendentes] = useState([]);
  const [webhookFailures, setWebhookFailures] = useState([]);
  const toast = useToast();

  useEffect(() => {
    // Exemplo de integração WebSocket ou Polling
    // const unsubscribe = api.subscribeToPayments((data) => { ... });
    // return () => unsubscribe();
  }, []);

  const handleManualReconciliation = async (transacaoId: string) => {
    try {
      // await api.reconcilePayment(transacaoId);
      toast({
        title: 'Reconciliação manual iniciada',
        description: `ID: ${transacaoId}`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Erro na reconciliação',
        status: 'error'
      });
    }
  };

  return (
    <Box p={6} bg="gray.50" minH="100vh">
      {/* Status dos Providers */}
      <Grid templateColumns="repeat(auto-fit, minmax(240px, 1fr))" gap={6} mb={8}>
        {providers.map(provider => (
          <Stat key={provider.id} p={4} bg="white" borderRadius="lg" shadow="sm" border="1px" borderColor="gray.100">
            <StatLabel fontWeight="bold" color="gray.600">{provider.name.toUpperCase()}</StatLabel>
            <StatNumber my={2}>
              <Badge colorScheme={provider.healthy ? 'green' : 'red'} variant="subtle" px={2} py={1} borderRadius="md">
                {provider.healthy ? 'Online' : 'Offline'}
              </Badge>
            </StatNumber>
            <StatHelpText color="gray.500">
              {provider.current_provider === provider.name && <Badge colorScheme="blue" variant="solid" mr={2}>ATIVO</Badge>}
              {provider.fallback_count > 0 && `Fallbacks: ${provider.fallback_count}`}
            </StatHelpText>
          </Stat>
        ))}
      </Grid>

      {/* Alertas Críticos */}
      {webhookFailures.length > 5 && (
        <Alert status="error" mb={6} borderRadius="lg" variant="left-accent">
          <AlertIcon />
          <Box flex="1">
            <AlertTitle>Muitos webhooks falhando!</AlertTitle>
            <AlertDescription display="block">
              {webhookFailures.length} falhas nas últimas 24h. Verifique as integrações dos provedores.
            </AlertDescription>
          </Box>
          <Button size="sm" colorScheme="red" variant="outline" ml={4}>Ver Detalhes</Button>
        </Alert>
      )}

      {/* Transações Pendentes */}
      <Box mb={10} bg="white" p={6} borderRadius="xl" shadow="sm">
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={6}>
          <Box fontWeight="bold" fontSize="xl">Transações Pendentes</Box>
          <Button size="sm" colorScheme="blue" variant="solid" px={6}>
            Reconciliação em Massa
          </Button>
        </Box>
        
        <Box overflowX="auto">
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>ID</Th>
                <Th>Revendedora</Th>
                <Th>Valor</Th>
                <Th>Provider</Th>
                <Th>Status</Th>
                <Th>Criada em</Th>
                <Th textAlign="right">Ações</Th>
              </Tr>
            </Thead>
            <Tbody>
              {transacoesPendentes.map(tx => (
                <Tr key={tx.id} _hover={{ bg: "gray.50" }}>
                  <Td fontWeight="medium">#{tx.id.slice(0, 8)}</Td>
                  <Td>{tx.revendedora_nome}</Td>
                  <Td fontWeight="bold">R$ {tx.valor_bruto.toFixed(2)}</Td>
                  <Td>
                    <Badge colorScheme={tx.provider === 'asaas' ? 'blue' : 'purple'}>
                      {tx.provider}
                    </Badge>
                  </Td>
                  <Td>
                    <Badge colorScheme={
                      tx.status === 'pending' ? 'yellow' :
                      tx.status === 'confirmed' ? 'green' : 'red'
                    } variant="solid">
                      {tx.status.toUpperCase()}
                    </Badge>
                  </Td>
                  <Td color="gray.500">{new Date(tx.created_at).toLocaleString('pt-BR')}</Td>
                  <Td textAlign="right">
                    <Button 
                      size="xs" 
                      colorScheme="gray"
                      variant="outline"
                      onClick={() => handleManualReconciliation(tx.id)}
                    >
                      Reconciliação Manual
                    </Button>
                  </Td>
                </Tr>
              ))}
              {transacoesPendentes.length === 0 && (
                <Tr>
                  <Td colSpan={7} textAlign="center" py={10} color="gray.400 italic">
                    Nenhuma transação pendente no momento.
                  </Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </Box>
      </Box>

      {/* Dead Letter Queue (Webhooks Falhos) */}
      <Box bg="white" p={6} borderRadius="xl" shadow="sm">
        <Box fontWeight="bold" fontSize="xl" mb={6} color="red.700">
          Monitor de Webhooks Falhos (DLQ)
        </Box>
        <Box overflowX="auto">
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Provider</Th>
                <Th>Dados (Payload)</Th>
                <Th>Tentativas</Th>
                <Th>Último Erro</Th>
                <Th textAlign="right">Ações</Th>
              </Tr>
            </Thead>
            <Tbody>
              {webhookFailures.slice(0, 5).map(f => (
                <Tr key={f.id} _hover={{ bg: "red.50" }}>
                  <Td>
                    <Badge colorScheme="gray">{f.provider}</Badge>
                  </Td>
                  <Td maxW="250px">
                    <Box as="code" fontSize="xs" color="gray.600" isTruncated display="block">
                      {JSON.stringify(f.payload)}
                    </Box>
                  </Td>
                  <Td fontWeight="bold">{f.attempts}/5</Td>
                  <Td color="red.500" fontSize="sm">{f.error?.slice(0, 60)}...</Td>
                  <Td textAlign="right">
                    <Button size="xs" colorScheme="green" mr={2}>Reprocessar</Button>
                    <Button size="xs" colorScheme="red" variant="ghost">Ignorar</Button>
                  </Td>
                </Tr>
              ))}
              {webhookFailures.length === 0 && (
                <Tr>
                  <Td colSpan={5} textAlign="center" py={10} color="gray.400 italic">
                    Fila de webhooks vazia. Excelente!
                  </Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </Box>
      </Box>
    </Box>
  );
}
